"""
MCP (Model Context Protocol) Integration for VIREON Data Connectors

This module provides MCP protocol implementation for enriching data operations
with context and enabling communication with external tools and AI services.
"""

import asyncio
import json
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
import logging
from abc import ABC, abstractmethod


class MCPMessageType(Enum):
    """Types of MCP messages"""
    REQUEST = auto()
    RESPONSE = auto()
    NOTIFICATION = auto()
    ERROR = auto()
    STREAM = auto()


class MCPResourceType(Enum):
    """Types of MCP resources"""
    DATA_SOURCE = auto()
    AI_MODEL = auto()
    TOOL = auto()
    CONNECTOR = auto()
    SERVICE = auto()


@dataclass
class MCPMessage:
    """MCP Protocol Message"""
    id: str
    type: MCPMessageType
    method: str
    params: Dict[str, Any] = field(default_factory=dict)
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class MCPResource:
    """MCP Resource Definition"""
    id: str
    name: str
    type: MCPResourceType
    uri: str
    capabilities: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    status: str = "available"


@dataclass
class MCPContext:
    """Context for MCP operations"""
    session_id: str
    user_context: Dict[str, Any] = field(default_factory=dict)
    environment: Dict[str, Any] = field(default_factory=dict)
    history: List[MCPMessage] = field(default_factory=list)
    active_resources: List[MCPResource] = field(default_factory=list)


class MCPTool(ABC):
    """Abstract base class for MCP tools"""
    
    def __init__(self, tool_name: str, description: str):
        self.tool_name = tool_name
        self.description = description
        self.logger = logging.getLogger(f"mcp.tool.{tool_name}")
    
    @abstractmethod
    async def execute(self, params: Dict[str, Any], context: MCPContext) -> Any:
        """Execute the tool with given parameters and context"""
        pass
    
    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        """Get the parameter schema for this tool"""
        pass


class MCPProtocol:
    """
    MCP Protocol implementation for VIREON data connectors.
    
    Manages communication, context enrichment, and tool registration.
    """
    
    def __init__(self):
        self.resources: Dict[str, MCPResource] = {}
        self.tools: Dict[str, MCPTool] = {}
        self.handlers: Dict[str, Callable] = {}
        self.contexts: Dict[str, MCPContext] = {}
        self.logger = logging.getLogger("mcp.protocol")
        self._message_counter = 0
        
        # Register default handlers
        self._register_default_handlers()
    
    def _register_default_handlers(self):
        """Register default message handlers"""
        self.register_handler("list_resources", self._handle_list_resources)
        self.register_handler("list_tools", self._handle_list_tools)
        self.register_handler("execute_tool", self._handle_execute_tool)
        self.register_handler("get_context", self._handle_get_context)
        self.register_handler("update_context", self._handle_update_context)
    
    def register_resource(self, resource: MCPResource):
        """Register a resource with MCP"""
        self.resources[resource.id] = resource
        self.logger.info(f"Registered resource: {resource.name} ({resource.type.name})")
    
    def register_tool(self, tool: MCPTool):
        """Register a tool with MCP"""
        self.tools[tool.tool_name] = tool
        self.logger.info(f"Registered tool: {tool.tool_name}")
    
    def register_handler(self, method: str, handler: Callable):
        """Register a message handler"""
        self.handlers[method] = handler
    
    def create_context(self, session_id: str) -> MCPContext:
        """Create a new MCP context"""
        context = MCPContext(session_id=session_id)
        self.contexts[session_id] = context
        return context
    
    def get_context(self, session_id: str) -> Optional[MCPContext]:
        """Get context by session ID"""
        return self.contexts.get(session_id)
    
    async def send_message(self, message: MCPMessage) -> MCPMessage:
        """
        Send an MCP message and wait for response.
        
        Args:
            message: Message to send
            
        Returns:
            Response message
        """
        # Log the message
        self.logger.debug(f"Sending message: {message.method} (ID: {message.id})")
        
        # Handle the message
        if message.method in self.handlers:
            try:
                result = await self.handlers[message.method](message)
                return MCPMessage(
                    id=self._generate_message_id(),
                    type=MCPMessageType.RESPONSE,
                    method=message.method,
                    result=result,
                    context=message.context
                )
            except Exception as e:
                self.logger.error(f"Error handling message: {str(e)}")
                return MCPMessage(
                    id=self._generate_message_id(),
                    type=MCPMessageType.ERROR,
                    method=message.method,
                    error={
                        "code": -32603,
                        "message": "Internal error",
                        "data": str(e)
                    },
                    context=message.context
                )
        else:
            return MCPMessage(
                id=self._generate_message_id(),
                type=MCPMessageType.ERROR,
                method=message.method,
                error={
                    "code": -32601,
                    "message": "Method not found",
                    "data": f"Unknown method: {message.method}"
                },
                context=message.context
            )
    
    async def send_notification(self, method: str, params: Dict[str, Any], 
                               context: Optional[MCPContext] = None):
        """
        Send a notification (no response expected).
        
        Args:
            method: Notification method
            params: Notification parameters
            context: Optional context
        """
        message = MCPMessage(
            id=self._generate_message_id(),
            type=MCPMessageType.NOTIFICATION,
            method=method,
            params=params,
            context=context.__dict__ if context else {}
        )
        
        self.logger.debug(f"Sending notification: {method}")
        
        # Notifications don't expect responses, but we can log them
        if context:
            context.history.append(message)
    
    def enrich_with_context(self, data: Any, context: MCPContext) -> Dict[str, Any]:
        """
        Enrich data with MCP context.
        
        Args:
            data: Data to enrich
            context: MCP context
            
        Returns:
            Enriched data
        """
        return {
            "data": data,
            "context": {
                "session_id": context.session_id,
                "user": context.user_context,
                "environment": context.environment,
                "resources": [r.name for r in context.active_resources],
                "timestamp": datetime.now().isoformat()
            }
        }
    
    async def _handle_list_resources(self, message: MCPMessage) -> List[Dict[str, Any]]:
        """Handle list_resources request"""
        resource_type = message.params.get("type")
        
        resources = self.resources.values()
        if resource_type:
            resources = [r for r in resources if r.type.name == resource_type]
        
        return [
            {
                "id": r.id,
                "name": r.name,
                "type": r.type.name,
                "uri": r.uri,
                "capabilities": r.capabilities,
                "status": r.status
            }
            for r in resources
        ]
    
    async def _handle_list_tools(self, message: MCPMessage) -> List[Dict[str, Any]]:
        """Handle list_tools request"""
        return [
            {
                "name": tool.tool_name,
                "description": tool.description,
                "schema": tool.get_schema()
            }
            for tool in self.tools.values()
        ]
    
    async def _handle_execute_tool(self, message: MCPMessage) -> Any:
        """Handle execute_tool request"""
        tool_name = message.params.get("tool")
        tool_params = message.params.get("params", {})
        session_id = message.context.get("session_id")
        
        if tool_name not in self.tools:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        tool = self.tools[tool_name]
        context = self.get_context(session_id) if session_id else None
        
        if not context:
            # Create a temporary context
            context = MCPContext(session_id=session_id or "temp")
        
        return await tool.execute(tool_params, context)
    
    async def _handle_get_context(self, message: MCPMessage) -> Dict[str, Any]:
        """Handle get_context request"""
        session_id = message.params.get("session_id")
        context = self.get_context(session_id)
        
        if not context:
            raise ValueError(f"Unknown session: {session_id}")
        
        return {
            "session_id": context.session_id,
            "user_context": context.user_context,
            "environment": context.environment,
            "active_resources": [r.id for r in context.active_resources],
            "history_length": len(context.history)
        }
    
    async def _handle_update_context(self, message: MCPMessage) -> Dict[str, Any]:
        """Handle update_context request"""
        session_id = message.params.get("session_id")
        updates = message.params.get("updates", {})
        
        context = self.get_context(session_id)
        if not context:
            context = self.create_context(session_id)
        
        # Update context fields
        if "user_context" in updates:
            context.user_context.update(updates["user_context"])
        if "environment" in updates:
            context.environment.update(updates["environment"])
        
        return {"status": "updated", "session_id": session_id}
    
    def _generate_message_id(self) -> str:
        """Generate unique message ID"""
        self._message_counter += 1
        return f"msg_{self._message_counter}_{datetime.now().timestamp()}"


class MCPDataTool(MCPTool):
    """Base class for MCP data operation tools"""
    
    def __init__(self, tool_name: str, description: str, connector):
        super().__init__(tool_name, description)
        self.connector = connector
    
    async def execute(self, params: Dict[str, Any], context: MCPContext) -> Any:
        """Execute data operation"""
        # Enrich parameters with context
        enriched_params = {
            **params,
            "mcp_context": {
                "session_id": context.session_id,
                "user": context.user_context,
                "environment": context.environment
            }
        }
        
        # Execute through connector
        return await self._execute_operation(enriched_params)
    
    @abstractmethod
    async def _execute_operation(self, params: Dict[str, Any]) -> Any:
        """Execute the specific operation"""
        pass


# Standard MCP Tools for Data Operations

class QueryDataTool(MCPDataTool):
    """Tool for querying data from any configured source"""
    
    def __init__(self, connector):
        super().__init__(
            "query_data",
            "Query data from any configured source with filtering and pagination",
            connector
        )
    
    async def _execute_operation(self, params: Dict[str, Any]) -> Any:
        result = await self.connector.query(params)
        return result.data if result.success else {"error": result.error}
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "source": {"type": "string", "description": "Data source identifier"},
                "filters": {"type": "object", "description": "Query filters"},
                "fields": {"type": "array", "items": {"type": "string"}},
                "limit": {"type": "integer", "default": 100},
                "offset": {"type": "integer", "default": 0}
            },
            "required": ["source"]
        }


class StoreDataTool(MCPDataTool):
    """Tool for storing data to any configured destination"""
    
    def __init__(self, connector):
        super().__init__(
            "store_data",
            "Store data to any configured destination with validation",
            connector
        )
    
    async def _execute_operation(self, params: Dict[str, Any]) -> Any:
        from connectors.data_connectors.base_data_connector import DataContext, DataOperation
        
        context = DataContext(
            operation=DataOperation.CREATE,
            source=params.get("destination", "default"),
            metadata=params
        )
        
        result = await self.connector.execute_operation(context)
        return {"success": result.success, "id": result.data} if result.success else {"error": result.error}
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "destination": {"type": "string", "description": "Data destination"},
                "data": {"type": "object", "description": "Data to store"},
                "validate": {"type": "boolean", "default": True}
            },
            "required": ["destination", "data"]
        }


class TransformDataTool(MCPDataTool):
    """Tool for transforming data between formats"""
    
    def __init__(self, connector):
        super().__init__(
            "transform_data",
            "Transform data between different formats",
            connector
        )
    
    async def _execute_operation(self, params: Dict[str, Any]) -> Any:
        # This would integrate with transformation logic
        return {
            "transformed": True,
            "format": params.get("target_format"),
            "records": params.get("data", [])
        }
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "data": {"type": "array", "description": "Data to transform"},
                "source_format": {"type": "string"},
                "target_format": {"type": "string"},
                "mapping": {"type": "object", "description": "Field mappings"}
            },
            "required": ["data", "target_format"]
        }


# Singleton instance
mcp_protocol = MCPProtocol()
