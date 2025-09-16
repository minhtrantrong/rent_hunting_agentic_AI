#!/usr/bin/env python3
"""
Debug MCP email functionality
"""
import sys
import os
from dotenv import load_dotenv

load_dotenv()

def test_mcp_client():
    """Test MCP client initialization and email functionality"""

    # Import the app modules
    sys.path.insert(0, '/Users/comradeflats/Desktop/rent_hunting_agentic_AI')

    try:
        from app import mcp_client, MCP_AVAILABLE

        print("🔍 Testing MCP Client State...")
        print(f"MCP_AVAILABLE: {MCP_AVAILABLE}")
        print(f"mcp_client: {mcp_client}")

        if not MCP_AVAILABLE:
            print("❌ MCP not available")
            return

        # Test direct MCP call
        print("\n🔍 Testing direct MCP email call...")

        email_params = {
            "to_email": os.getenv("DEFAULT_EMAIL"),
            "subject": "Debug Test Email",
            "message": "Testing MCP email functionality",
            "from_email": os.getenv("EMAIL_USERNAME")
        }

        print(f"Email params: {email_params}")

        result = mcp_client.call("email-server", "send_email", **email_params)
        print(f"📧 Raw MCP result: {result}")
        print(f"Result type: {type(result)}")

        if isinstance(result, dict):
            for key, value in result.items():
                print(f"  {key}: {value}")

    except Exception as e:
        print(f"❌ Error testing MCP: {str(e)}")
        import traceback
        traceback.print_exc()

def test_mcp_server_status():
    """Check if email server is running"""
    try:
        from app import mcp_client

        # Try to list tools
        print("🔍 Checking MCP server tools...")
        tools = mcp_client.list_tools("email-server")
        print(f"Available tools: {tools}")

    except Exception as e:
        print(f"❌ Error checking MCP server: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🔧 MCP Email Debug Session")
    print("=" * 50)

    test_mcp_client()
    print()
    test_mcp_server_status()