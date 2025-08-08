"""
Model Context Protocol (MCP) Framework Implementation
Production-quality MCP servers for RentGenius Agent #3
"""

import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union, Callable
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

class MCPErrorCode(Enum):
    """Standard MCP error codes"""
    PARSE_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603
    SERVER_ERROR = -32000

@dataclass
class MCPError:
    """MCP error response"""
    code: int
    message: str
    data: Optional[Dict] = None

@dataclass
class MCPRequest:
    """MCP request format"""
    id: str
    method: str
    params: Dict[str, Any]

@dataclass
class MCPResponse:
    """MCP response format"""
    id: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[MCPError] = None

class MCPTool:
    """Individual MCP tool definition"""
    
    def __init__(
        self, 
        name: str, 
        description: str, 
        input_schema: Dict[str, Any],
        handler: Callable
    ):
        self.name = name
        self.description = description
        self.input_schema = input_schema
        self.handler = handler
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert tool to MCP format"""
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.input_schema
        }

class MCPServer(ABC):
    """Base MCP Server implementation"""
    
    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.tools: Dict[str, MCPTool] = {}
        self.capabilities = self._define_capabilities()
        self.logger = logging.getLogger(f"MCP.{name}")
        self._initialize_tools()
    
    @abstractmethod
    def _define_capabilities(self) -> List[str]:
        """Define what this MCP server can do"""
        pass
    
    @abstractmethod
    def _initialize_tools(self):
        """Initialize available tools"""
        pass
    
    def register_tool(self, tool: MCPTool):
        """Register a tool with this server"""
        self.tools[tool.name] = tool
        self.logger.info(f"Registered tool: {tool.name}")
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get server information"""
        return {
            "name": self.name,
            "version": self.version,
            "capabilities": self.capabilities,
            "tools": [tool.to_dict() for tool in self.tools.values()]
        }
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools"""
        return [tool.to_dict() for tool in self.tools.values()]
    
    def call_tool(self, request: MCPRequest) -> MCPResponse:
        """Handle tool call request"""
        try:
            tool_name = request.method
            
            if tool_name not in self.tools:
                return MCPResponse(
                    id=request.id,
                    error=MCPError(
                        code=MCPErrorCode.METHOD_NOT_FOUND.value,
                        message=f"Tool not found: {tool_name}"
                    )
                )
            
            tool = self.tools[tool_name]
            
            # Validate parameters against schema
            validation_error = self._validate_params(request.params, tool.input_schema)
            if validation_error:
                return MCPResponse(
                    id=request.id,
                    error=MCPError(
                        code=MCPErrorCode.INVALID_PARAMS.value,
                        message=validation_error
                    )
                )
            
            # Call the tool handler
            result = tool.handler(request.params)
            
            return MCPResponse(
                id=request.id,
                result=result
            )
            
        except Exception as e:
            self.logger.error(f"Tool call failed: {e}")
            return MCPResponse(
                id=request.id,
                error=MCPError(
                    code=MCPErrorCode.INTERNAL_ERROR.value,
                    message=str(e)
                )
            )
    
    def _validate_params(self, params: Dict[str, Any], schema: Dict[str, Any]) -> Optional[str]:
        """Basic parameter validation against JSON schema"""
        required = schema.get("required", [])
        properties = schema.get("properties", {})
        
        # Check required parameters
        for field in required:
            if field not in params:
                return f"Missing required parameter: {field}"
        
        # Check parameter types (basic validation)
        for field, value in params.items():
            if field in properties:
                expected_type = properties[field].get("type")
                if expected_type == "string" and not isinstance(value, str):
                    return f"Parameter {field} must be a string"
                elif expected_type == "integer" and not isinstance(value, int):
                    return f"Parameter {field} must be an integer"
                elif expected_type == "boolean" and not isinstance(value, bool):
                    return f"Parameter {field} must be a boolean"
                elif expected_type == "object" and not isinstance(value, dict):
                    return f"Parameter {field} must be an object"
                elif expected_type == "array" and not isinstance(value, list):
                    return f"Parameter {field} must be an array"
        
        return None

class MCPRegistry:
    """Registry for managing MCP servers"""
    
    def __init__(self):
        self.servers: Dict[str, MCPServer] = {}
        self.logger = logging.getLogger("MCP.Registry")
    
    def register_server(self, server: MCPServer):
        """Register an MCP server"""
        self.servers[server.name] = server
        self.logger.info(f"Registered MCP server: {server.name}")
    
    def get_server(self, name: str) -> Optional[MCPServer]:
        """Get MCP server by name"""
        return self.servers.get(name)
    
    def list_servers(self) -> Dict[str, Dict[str, Any]]:
        """List all registered servers and their info"""
        return {
            name: server.get_server_info() 
            for name, server in self.servers.items()
        }
    
    def call_tool(self, server_name: str, tool_name: str, params: Dict[str, Any], request_id: str = None) -> MCPResponse:
        """Call a tool on a specific server"""
        if request_id is None:
            request_id = f"req_{datetime.now().timestamp()}"
        
        server = self.get_server(server_name)
        if not server:
            return MCPResponse(
                id=request_id,
                error=MCPError(
                    code=MCPErrorCode.SERVER_ERROR.value,
                    message=f"Server not found: {server_name}"
                )
            )
        
        request = MCPRequest(
            id=request_id,
            method=tool_name,
            params=params
        )
        
        return server.call_tool(request)
    
    def get_all_tools(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get all tools from all servers"""
        all_tools = {}
        for name, server in self.servers.items():
            all_tools[name] = server.list_tools()
        return all_tools

class MCPClient:
    """Client for interacting with MCP servers through registry"""
    
    def __init__(self, registry: MCPRegistry):
        self.registry = registry
        self.logger = logging.getLogger("MCP.Client")
    
    def call(self, server_name: str, tool_name: str, **params) -> Dict[str, Any]:
        """Simplified tool calling interface"""
        response = self.registry.call_tool(server_name, tool_name, params)
        
        if response.error:
            self.logger.error(f"MCP call failed: {response.error.message}")
            raise Exception(f"MCP Error ({response.error.code}): {response.error.message}")
        
        return response.result
    
    def list_available_tools(self) -> Dict[str, List[str]]:
        """List all available tools by server"""
        result = {}
        for server_name, tools in self.registry.get_all_tools().items():
            result[server_name] = [tool["name"] for tool in tools]
        return result
    
    def get_tool_info(self, server_name: str, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific tool"""
        server = self.registry.get_server(server_name)
        if not server or tool_name not in server.tools:
            return None
        
        return server.tools[tool_name].to_dict()

# Utility function for creating MCP tools easily
def mcp_tool(name: str, description: str, input_schema: Dict[str, Any]):
    """Decorator for creating MCP tools"""
    def decorator(func: Callable) -> MCPTool:
        return MCPTool(
            name=name,
            description=description,
            input_schema=input_schema,
            handler=func
        )
    return decorator

# Setup logging for MCP framework
def setup_mcp_logging(level: str = "INFO"):
    """Setup logging for MCP framework"""
    logging.basicConfig(
        level=getattr(logging, level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

if __name__ == "__main__":
    # Example usage
    setup_mcp_logging()
    
    # This would be implemented by actual MCP servers
    print("🔧 MCP Framework loaded - ready for server implementations")
    print("📊 Use this framework to create CalendarMCPServer, CommunicationMCPServer, etc.")