#!/usr/bin/env python3
"""
Test MCP email server functionality directly
"""
import asyncio
import sys
import os
from dotenv import load_dotenv

# Add current directory to path
sys.path.insert(0, '/Users/comradeflats/Desktop/rent_hunting_agentic_AI')

load_dotenv()

async def test_mcp_email():
    """Test the MCP email server directly"""

    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    try:
        # Test email server initialization
        print("🔍 Testing MCP Email Server...")

        server_params = StdioServerParameters(
            command="python",
            args=["email_server.py"],
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize
                await session.initialize()
                print("✅ MCP server initialized")

                # List available tools
                tools = await session.list_tools()
                print(f"📋 Available tools: {[tool.name for tool in tools.tools]}")

                # Test send_email tool
                result = await session.call_tool(
                    "send_email",
                    {
                        "to_email": os.getenv("DEFAULT_EMAIL"),
                        "subject": "MCP Test Email",
                        "message": "This is a test from the MCP email server.",
                        "from_email": os.getenv("EMAIL_USERNAME")
                    }
                )

                print(f"📧 Email result: {result}")

    except Exception as e:
        print(f"❌ MCP Email test failed: {str(e)}")
        import traceback
        traceback.print_exc()

def test_app_email_function():
    """Test the email function from app.py directly"""
    try:
        # Import the email function
        sys.path.insert(0, '/Users/comradeflats/Desktop/rent_hunting_agentic_AI')
        from app import send_email_tool

        print("🔍 Testing app.py email function directly...")

        result = send_email_tool(
            to_email=os.getenv("DEFAULT_EMAIL"),
            subject="Direct Function Test",
            message="Testing email function directly from app.py"
        )

        print(f"📧 Direct function result: {result}")

    except Exception as e:
        print(f"❌ Direct function test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Testing email functionality...")
    print("=" * 50)

    # Test 1: Direct function call
    test_app_email_function()
    print()

    # Test 2: MCP server
    print("Testing MCP server...")
    asyncio.run(test_mcp_email())