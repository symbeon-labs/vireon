"""
REST API Connector for VIREON Data Connectors

This module provides REST API connectivity with MCP integration
for seamless data operations across HTTP-based services.
"""

import aiohttp
import asyncio
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import json
import logging
from urllib.parse import urljoin, urlencode

from .base_data_connector import (
    BaseDataConnector, ConnectionConfig, DataContext, 
    DataResult, DataOperation, DataConnectorType
)
from ..mcp_integration.mcp_protocol import mcp_protocol, MCPResource, MCPResourceType


class RESTConnector(BaseDataConnector):
    """
    REST API connector implementation.
    
    Supports REST and GraphQL endpoints with authentication,
    rate limiting, and automatic retry.
    """
    
    def __init__(self, adapter_name: str, config: ConnectionConfig):
        """
        Initialize REST connector.
        
        Args:
            adapter_name: Unique identifier for this connector
            config: Connection configuration
        """
        # Ensure connector type is REST_API
        config.connector_type = DataConnectorType.REST_API
        super().__init__(adapter_name, config)
        
        self.session: Optional[aiohttp.ClientSession] = None
        self.headers = {}
        self.auth_type = config.credentials.get('auth_type', 'none') if config.credentials else 'none'
        
        # Rate limiting
        self.rate_limiter = {
            'requests_per_second': config.connection_params.get('rate_limit', 10),
            'last_request': datetime.now(),
            'request_count': 0
        }
        
        # Register with MCP
        self._register_mcp_resource()
    
    def _register_mcp_resource(self):
        """Register this connector as an MCP resource"""
        resource = MCPResource(
            id=f"rest_{self.adapter_name}",
            name=self.adapter_name,
            type=MCPResourceType.CONNECTOR,
            uri=self.connection_config.endpoint or "http://localhost",
            capabilities=["rest", "http", "https", "json", "graphql"],
            metadata={
                "auth_type": self.auth_type,
                "timeout": self.connection_config.timeout,
                "retry_count": self.connection_config.retry_count
            }
        )
        mcp_protocol.register_resource(resource)
    
    async def establish_connection(self) -> bool:
        """
        Establish HTTP session for REST API.
        
        Returns:
            bool: True if session created successfully
        """
        try:
            # Configure headers
            self._configure_headers()
            
            # Create session with timeout
            timeout = aiohttp.ClientTimeout(total=self.connection_config.timeout)
            self.session = aiohttp.ClientSession(
                headers=self.headers,
                timeout=timeout
            )
            
            # Test connection if endpoint provided
            if self.connection_config.endpoint:
                async with self.session.get(self.connection_config.endpoint) as resp:
                    if resp.status >= 500:
                        raise Exception(f"Server error: {resp.status}")
            
            self.logger.info("REST API session established")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to establish REST connection: {str(e)}")
            if self.session:
                await self.session.close()
                self.session = None
            return False
    
    async def close_connection(self) -> bool:
        """
        Close HTTP session.
        
        Returns:
            bool: True if session closed successfully
        """
        try:
            if self.session:
                await self.session.close()
                self.session = None
            return True
        except Exception as e:
            self.logger.error(f"Error closing REST connection: {str(e)}")
            return False
    
    async def execute_operation(self, context: DataContext) -> DataResult:
        """
        Execute REST API operation.
        
        Args:
            context: Data operation context
            
        Returns:
            DataResult: Result of the operation
        """
        if not self.session:
            return DataResult(
                success=False,
                error="Not connected. Please establish connection first."
            )
        
        # Apply rate limiting
        await self._apply_rate_limit()
        
        # Route to appropriate method
        operation_map = {
            DataOperation.CREATE: self._http_post,
            DataOperation.READ: self._http_get,
            DataOperation.UPDATE: self._http_put,
            DataOperation.DELETE: self._http_delete,
            DataOperation.QUERY: self._http_get,
            DataOperation.BATCH: self._http_batch
        }
        
        handler = operation_map.get(context.operation)
        if not handler:
            return DataResult(
                success=False,
                error=f"Operation {context.operation.name} not supported for REST"
            )
        
        # Execute with retry
        return await self._execute_with_retry(handler, context)
    
    async def _execute_with_retry(self, handler, context: DataContext) -> DataResult:
        """Execute operation with automatic retry"""
        last_error = None
        
        for attempt in range(self.connection_config.retry_count):
            try:
                result = await handler(context)
                
                # Enrich with MCP context if available
                if context.mcp_context:
                    session_id = context.mcp_context.get('session_id')
                    if session_id:
                        mcp_context = mcp_protocol.get_context(session_id)
                        if mcp_context:
                            result.mcp_enrichment = mcp_protocol.enrich_with_context(
                                result.data, mcp_context
                            )
                
                return result
                
            except Exception as e:
                last_error = str(e)
                self.logger.warning(f"Attempt {attempt + 1} failed: {last_error}")
                
                if attempt < self.connection_config.retry_count - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
        
        return DataResult(
            success=False,
            error=f"All retry attempts failed. Last error: {last_error}"
        )
    
    async def _http_get(self, context: DataContext) -> DataResult:
        """Execute HTTP GET request"""
        try:
            url = self._build_url(context.source)
            params = context.filters if context.filters else None
            
            async with self.session.get(url, params=params) as resp:
                return await self._process_response(resp)
                
        except Exception as e:
            return DataResult(success=False, error=str(e))
    
    async def _http_post(self, context: DataContext) -> DataResult:
        """Execute HTTP POST request"""
        try:
            url = self._build_url(context.source)
            data = context.metadata.get('data', {})
            
            # Handle different content types
            if context.metadata.get('content_type') == 'form':
                async with self.session.post(url, data=data) as resp:
                    return await self._process_response(resp)
            else:
                async with self.session.post(url, json=data) as resp:
                    return await self._process_response(resp)
                    
        except Exception as e:
            return DataResult(success=False, error=str(e))
    
    async def _http_put(self, context: DataContext) -> DataResult:
        """Execute HTTP PUT request"""
        try:
            url = self._build_url(context.source)
            data = context.metadata.get('data', {})
            
            async with self.session.put(url, json=data) as resp:
                return await self._process_response(resp)
                
        except Exception as e:
            return DataResult(success=False, error=str(e))
    
    async def _http_delete(self, context: DataContext) -> DataResult:
        """Execute HTTP DELETE request"""
        try:
            url = self._build_url(context.source)
            
            async with self.session.delete(url) as resp:
                return await self._process_response(resp)
                
        except Exception as e:
            return DataResult(success=False, error=str(e))
    
    async def _http_batch(self, context: DataContext) -> DataResult:
        """Execute batch operations"""
        try:
            # Batch operations would be implemented based on API specifics
            # This is a placeholder implementation
            batch_data = context.metadata.get('batch', [])
            results = []
            
            for item in batch_data:
                # Create sub-context for each item
                sub_context = DataContext(
                    operation=DataOperation[item.get('operation', 'CREATE')],
                    source=item.get('source', context.source),
                    metadata={'data': item.get('data', {})}
                )
                
                result = await self.execute_operation(sub_context)
                results.append({
                    'success': result.success,
                    'data': result.data if result.success else None,
                    'error': result.error if not result.success else None
                })
            
            return DataResult(
                success=True,
                data=results,
                metadata={'batch_size': len(results)}
            )
            
        except Exception as e:
            return DataResult(success=False, error=str(e))
    
    async def _process_response(self, response: aiohttp.ClientResponse) -> DataResult:
        """Process HTTP response"""
        try:
            # Check status
            if response.status >= 400:
                error_text = await response.text()
                return DataResult(
                    success=False,
                    error=f"HTTP {response.status}: {error_text}",
                    metadata={'status_code': response.status}
                )
            
            # Parse response based on content type
            content_type = response.headers.get('Content-Type', '')
            
            if 'application/json' in content_type:
                data = await response.json()
            elif 'text' in content_type:
                data = await response.text()
            else:
                data = await response.read()
            
            return DataResult(
                success=True,
                data=data,
                metadata={
                    'status_code': response.status,
                    'headers': dict(response.headers)
                }
            )
            
        except Exception as e:
            return DataResult(
                success=False,
                error=f"Error processing response: {str(e)}"
            )
    
    def _configure_headers(self):
        """Configure HTTP headers including authentication"""
        self.headers = {
            'User-Agent': 'VIREON-DataConnector/1.0',
            'Accept': 'application/json'
        }
        
        if not self.connection_config.credentials:
            return
        
        # Bearer token authentication
        if self.auth_type == 'bearer':
            token = self.connection_config.credentials.get('token')
            if token:
                self.headers['Authorization'] = f"Bearer {token}"
        
        # API key authentication
        elif self.auth_type == 'api_key':
            api_key = self.connection_config.credentials.get('api_key')
            key_header = self.connection_config.credentials.get('key_header', 'X-API-Key')
            if api_key:
                self.headers[key_header] = api_key
        
        # Basic authentication
        elif self.auth_type == 'basic':
            username = self.connection_config.credentials.get('username')
            password = self.connection_config.credentials.get('password')
            if username and password:
                import base64
                credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
                self.headers['Authorization'] = f"Basic {credentials}"
        
        # Custom headers
        custom_headers = self.connection_config.connection_params.get('headers', {})
        self.headers.update(custom_headers)
    
    def _build_url(self, path: str) -> str:
        """Build full URL from base endpoint and path"""
        if path.startswith('http://') or path.startswith('https://'):
            return path
        
        base_url = self.connection_config.endpoint or ""
        return urljoin(base_url, path)
    
    async def _apply_rate_limit(self):
        """Apply rate limiting to requests"""
        now = datetime.now()
        time_diff = (now - self.rate_limiter['last_request']).total_seconds()
        
        # Reset counter if second has passed
        if time_diff >= 1:
            self.rate_limiter['request_count'] = 0
            self.rate_limiter['last_request'] = now
        
        # Check if we've exceeded rate limit
        if self.rate_limiter['request_count'] >= self.rate_limiter['requests_per_second']:
            sleep_time = 1 - time_diff
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
                self.rate_limiter['request_count'] = 0
                self.rate_limiter['last_request'] = datetime.now()
        
        self.rate_limiter['request_count'] += 1
    
    async def _stream_implementation(self, context: DataContext):
        """Implementation of streaming for REST APIs"""
        # For REST APIs, we can implement Server-Sent Events (SSE) streaming
        if not self.session:
            yield DataResult(success=False, error="Not connected")
            return
        
        url = self._build_url(context.source)
        
        try:
            async with self.session.get(url, headers={'Accept': 'text/event-stream'}) as resp:
                async for line in resp.content:
                    line = line.decode('utf-8').strip()
                    if line.startswith('data: '):
                        data = line[6:]  # Remove 'data: ' prefix
                        try:
                            yield DataResult(success=True, data=json.loads(data))
                        except json.JSONDecodeError:
                            yield DataResult(success=True, data=data)
                            
        except Exception as e:
            yield DataResult(success=False, error=str(e))
    
    # GraphQL support
    async def graphql_query(self, query: str, variables: Optional[Dict[str, Any]] = None) -> DataResult:
        """
        Execute GraphQL query.
        
        Args:
            query: GraphQL query string
            variables: Optional query variables
            
        Returns:
            DataResult: Query result
        """
        if not self.session:
            return DataResult(success=False, error="Not connected")
        
        context = DataContext(
            operation=DataOperation.QUERY,
            source=self.connection_config.endpoint or "/graphql",
            metadata={
                'data': {
                    'query': query,
                    'variables': variables or {}
                }
            }
        )
        
        return await self._http_post(context)
