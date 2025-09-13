"""
MCP Tools - Standalone Model Context Protocol Framework
A production-ready implementation of the Model Context Protocol for building AI tool servers.
"""

from .framework import (
    MCPServer,
    MCPTool,
    MCPClient,
    MCPRegistry,
    MCPRequest,
    MCPResponse,
    MCPError,
    MCPErrorCode,
    mcp_tool,
    setup_mcp_logging
)

__version__ = "1.0.0"
__author__ = "MCP Tools Team"
__description__ = "Standalone Model Context Protocol Framework"

__all__ = [
    "MCPServer",
    "MCPTool", 
    "MCPClient",
    "MCPRegistry",
    "MCPRequest",
    "MCPResponse",
    "MCPError",
    "MCPErrorCode",
    "mcp_tool",
    "setup_mcp_logging"
]