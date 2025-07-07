"""
Base Data Connector for VIREON System

This module provides the base class for all data connectors,
extending the UniversalAdapter to provide data-specific functionality.
"""

import asyncio
from abc import abstractmethod
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime
import json
import logging
from enum import Enum, auto

# Import VIREON core components
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from adapters.base_adapter import UniversalAdapter, AdapterCapability, AdapterMetadata
from models import Rule, ConsciousnessLevel


class DataConnectorType(Enum):
    """Types of data connectors"""
    REST_API = auto()
    DATABASE = auto()
    FILE_IO = auto()
    EVENT_STREAM = auto()
    AI_SERVICE = auto()
    CUSTOM_PROTOCOL = auto()


class DataOperation(Enum):
    """Supported data operations"""
    CREATE = auto()
    READ = auto()
    UPDATE = auto()
    DELETE = auto()
    QUERY = auto()
    STREAM = auto()
    BATCH = auto()
    TRANSFORM = auto()


@dataclass
class ConnectionConfig:
    """Configuration for data connections"""
    connector_type: DataConnectorType
    endpoint: Optional[str] = None
    credentials: Optional[Dict[str, Any]] = None
    connection_params: Dict[str, Any] = field(default_factory=dict)
    timeout: int = 30
    retry_count: int = 3
    batch_size: int = 100
    cache_enabled: bool = True
    cache_ttl: int = 3600  # seconds


@dataclass
class DataContext:
    """Context for data operations with MCP integration"""
    operation: DataOperation
    source: str
    target: Optional[str] = None
    filters: Dict[str, Any] = field(default_factory=dict)
    transformations: List[Dict[str, Any]] = field(default_factory=list)
    mcp_context: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class DataResult:
    """Result of a data operation"""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    mcp_enrichment: Dict[str, Any] = field(default_factory=dict)


class BaseDataConnector(UniversalAdapter):
    """
    Base class for all VIREON data connectors.
    
    Provides common functionality for data operations, caching,
    transformation, and MCP integration.
    """
    
    def __init__(self, adapter_name: str, config: ConnectionConfig):
        """
        Initialize the base data connector.
        
        Args:
            adapter_name: Unique identifier for this connector
            config: Connection configuration
        """
        super().__init__(adapter_name, config.__dict__)
        self.connection_config = config
        self.connection = None
        self.cache = {}
        self.metrics = {
            'operations_count': 0,
            'success_count': 0,
            'error_count': 0,
            'avg_latency': 0.0,
            'cache_hits': 0,
            'cache_misses': 0
        }
        
    def _create_metadata(self) -> AdapterMetadata:
        """Create metadata for the data connector"""
        return AdapterMetadata(
            name=self.adapter_name,
            version="1.0.0",
            supported_environments=["data_operations", "mcp_enabled"],
            capabilities=[
                AdapterCapability.REAL_TIME_SYNC,
                AdapterCapability.BIDIRECTIONAL_FEEDBACK,
                AdapterCapability.STATE_PERSISTENCE,
                AdapterCapability.API_INTEGRATION
            ],
            author="VIREON System",
            description=f"Data connector for {self.connection_config.connector_type.name}",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    
    @abstractmethod
    async def establish_connection(self) -> bool:
        """
        Establish connection to the data source.
        
        Returns:
            bool: True if connection successful
        """
        pass
    
    @abstractmethod
    async def close_connection(self) -> bool:
        """
        Close connection to the data source.
        
        Returns:
            bool: True if disconnection successful
        """
        pass
    
    @abstractmethod
    async def execute_operation(self, context: DataContext) -> DataResult:
        """
        Execute a data operation.
        
        Args:
            context: Data operation context
            
        Returns:
            DataResult: Result of the operation
        """
        pass
    
    # UniversalAdapter implementation
    async def connect(self, environment_config: Dict[str, Any]) -> bool:
        """Connect to the data source"""
        try:
            self.logger.info(f"Connecting to {self.connection_config.connector_type.name}")
            result = await self.establish_connection()
            if result:
                self.connected = True
                self.logger.info("Connection established successfully")
            return result
        except Exception as e:
            self.logger.error(f"Connection failed: {str(e)}")
            return False
    
    async def disconnect(self) -> bool:
        """Disconnect from the data source"""
        try:
            result = await self.close_connection()
            if result:
                self.connected = False
                self.logger.info("Disconnected successfully")
            return result
        except Exception as e:
            self.logger.error(f"Disconnection failed: {str(e)}")
            return False
    
    async def apply_rules(self, rules: List[Rule]) -> Dict[str, Any]:
        """Apply VIREON rules to data operations"""
        results = {
            'applied': [],
            'failed': [],
            'transformations': []
        }
        
        for rule in rules:
            try:
                # Extract data operation rules
                if rule.rule_type.name == "DATA_OPERATION":
                    context = self._rule_to_context(rule)
                    result = await self.execute_operation(context)
                    
                    if result.success:
                        results['applied'].append({
                            'rule_id': rule.id,
                            'result': result.data
                        })
                    else:
                        results['failed'].append({
                            'rule_id': rule.id,
                            'error': result.error
                        })
                        
                elif rule.rule_type.name == "TRANSFORMATION":
                    results['transformations'].append({
                        'rule_id': rule.id,
                        'transformation': rule.content
                    })
                    
            except Exception as e:
                results['failed'].append({
                    'rule_id': rule.id,
                    'error': str(e)
                })
                
        return results
    
    async def collect_feedback(self) -> Dict[str, Any]:
        """Collect feedback from data operations"""
        return {
            'metrics': self.metrics.copy(),
            'cache_statistics': {
                'size': len(self.cache),
                'hit_rate': self.metrics['cache_hits'] / max(1, self.metrics['cache_hits'] + self.metrics['cache_misses'])
            },
            'connection_status': self.connected,
            'timestamp': datetime.now().isoformat()
        }
    
    async def get_environment_state(self) -> Dict[str, Any]:
        """Get current state of the data connector"""
        return {
            'connector_type': self.connection_config.connector_type.name,
            'connected': self.connected,
            'metrics': self.metrics.copy(),
            'cache_enabled': self.connection_config.cache_enabled,
            'config': {
                'timeout': self.connection_config.timeout,
                'retry_count': self.connection_config.retry_count,
                'batch_size': self.connection_config.batch_size
            }
        }
    
    def translate_rule(self, rule: Rule, context) -> Dict[str, Any]:
        """Translate VIREON rule to data operation"""
        return {
            'operation': self._extract_operation(rule),
            'parameters': rule.content,
            'context': context.__dict__ if hasattr(context, '__dict__') else context
        }
    
    def validate_rule(self, rule: Rule) -> Tuple[bool, Optional[str]]:
        """Validate if rule can be applied to data operations"""
        if rule.rule_type.name not in ["DATA_OPERATION", "TRANSFORMATION", "QUERY"]:
            return False, f"Rule type {rule.rule_type.name} not supported for data operations"
        
        # Validate rule content
        if not isinstance(rule.content, dict):
            return False, "Rule content must be a dictionary for data operations"
        
        return True, None
    
    # Data-specific methods
    
    async def query(self, query_params: Dict[str, Any], 
                   use_cache: bool = True) -> DataResult:
        """
        Execute a query operation.
        
        Args:
            query_params: Query parameters
            use_cache: Whether to use cache
            
        Returns:
            DataResult: Query result
        """
        start_time = datetime.now()
        
        # Check cache
        if use_cache and self.connection_config.cache_enabled:
            cache_key = self._generate_cache_key("query", query_params)
            cached_result = self._get_from_cache(cache_key)
            if cached_result:
                self.metrics['cache_hits'] += 1
                return cached_result
            else:
                self.metrics['cache_misses'] += 1
        
        # Execute query
        context = DataContext(
            operation=DataOperation.QUERY,
            source=self.connection_config.endpoint or "default",
            filters=query_params
        )
        
        result = await self.execute_operation(context)
        
        # Update metrics
        latency = (datetime.now() - start_time).total_seconds()
        self._update_metrics(result.success, latency)
        result.performance_metrics['latency'] = latency
        
        # Cache result if successful
        if result.success and use_cache and self.connection_config.cache_enabled:
            self._add_to_cache(cache_key, result)
        
        return result
    
    async def batch_operation(self, operations: List[DataContext]) -> List[DataResult]:
        """
        Execute multiple operations in batch.
        
        Args:
            operations: List of operations to execute
            
        Returns:
            List of results
        """
        results = []
        batch_size = self.connection_config.batch_size
        
        for i in range(0, len(operations), batch_size):
            batch = operations[i:i + batch_size]
            batch_results = await asyncio.gather(
                *[self.execute_operation(op) for op in batch],
                return_exceptions=True
            )
            
            for j, result in enumerate(batch_results):
                if isinstance(result, Exception):
                    results.append(DataResult(
                        success=False,
                        error=str(result)
                    ))
                else:
                    results.append(result)
                    
        return results
    
    async def stream_data(self, stream_params: Dict[str, Any]):
        """
        Stream data from source.
        
        Args:
            stream_params: Streaming parameters
            
        Yields:
            Data items from stream
        """
        context = DataContext(
            operation=DataOperation.STREAM,
            source=self.connection_config.endpoint or "default",
            metadata=stream_params
        )
        
        # This is a generator method to be implemented by subclasses
        async for item in self._stream_implementation(context):
            yield item
    
    @abstractmethod
    async def _stream_implementation(self, context: DataContext):
        """Implementation of streaming logic by subclasses"""
        pass
    
    # Helper methods
    
    def _rule_to_context(self, rule: Rule) -> DataContext:
        """Convert a VIREON rule to data context"""
        content = rule.content
        return DataContext(
            operation=DataOperation[content.get('operation', 'READ')],
            source=content.get('source', 'default'),
            target=content.get('target'),
            filters=content.get('filters', {}),
            transformations=content.get('transformations', []),
            metadata=content.get('metadata', {})
        )
    
    def _extract_operation(self, rule: Rule) -> str:
        """Extract operation type from rule"""
        return rule.content.get('operation', 'READ')
    
    def _generate_cache_key(self, operation: str, params: Dict[str, Any]) -> str:
        """Generate cache key for operation"""
        return f"{operation}:{json.dumps(params, sort_keys=True)}"
    
    def _get_from_cache(self, key: str) -> Optional[DataResult]:
        """Get result from cache"""
        if key in self.cache:
            entry = self.cache[key]
            if (datetime.now() - entry['timestamp']).seconds < self.connection_config.cache_ttl:
                return entry['result']
            else:
                del self.cache[key]
        return None
    
    def _add_to_cache(self, key: str, result: DataResult):
        """Add result to cache"""
        self.cache[key] = {
            'result': result,
            'timestamp': datetime.now()
        }
    
    def _update_metrics(self, success: bool, latency: float):
        """Update performance metrics"""
        self.metrics['operations_count'] += 1
        if success:
            self.metrics['success_count'] += 1
        else:
            self.metrics['error_count'] += 1
        
        # Update average latency
        avg = self.metrics['avg_latency']
        count = self.metrics['operations_count']
        self.metrics['avg_latency'] = (avg * (count - 1) + latency) / count
    
    async def enrich_with_mcp(self, data: Any, context: DataContext) -> Any:
        """
        Enrich data with MCP context.
        
        Args:
            data: Data to enrich
            context: Operation context
            
        Returns:
            Enriched data
        """
        # This will be implemented to integrate with MCP
        # For now, return data with basic enrichment
        return {
            'data': data,
            'mcp_context': context.mcp_context,
            'timestamp': context.timestamp.isoformat(),
            'source': context.source
        }
