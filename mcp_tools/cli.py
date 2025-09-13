#!/usr/bin/env python3
"""
MCP Tools CLI - Command line interface for the MCP Tools framework
"""

import argparse
import sys
import os
from typing import Optional

def run_demo(demo_name: str):
    """Run a specific demo"""
    demos_dir = os.path.join(os.path.dirname(__file__), '..', 'examples')
    
    demo_files = {
        'basic': 'basic_demo.py',
        'multi': 'multi_server_demo.py'
    }
    
    if demo_name not in demo_files:
        print(f"❌ Unknown demo: {demo_name}")
        print(f"Available demos: {', '.join(demo_files.keys())}")
        return 1
    
    demo_file = os.path.join(demos_dir, demo_files[demo_name])
    
    if not os.path.exists(demo_file):
        print(f"❌ Demo file not found: {demo_file}")
        return 1
    
    print(f"🚀 Running {demo_name} demo...")
    
    # Execute the demo
    try:
        # Add the examples directory to Python path
        sys.path.insert(0, demos_dir)
        
        # Import and run the demo
        if demo_name == 'basic':
            from basic_demo import main
        elif demo_name == 'multi':
            from multi_server_demo import main
        
        main()
        return 0
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return 1

def show_info():
    """Show framework information"""
    from mcp_tools import __version__, __description__
    
    print(f"🔧 MCP Tools Framework")
    print(f"Version: {__version__}")
    print(f"Description: {__description__}")
    print(f"")
    print(f"Components:")
    print(f"  • MCPServer - Base class for creating tool servers")
    print(f"  • MCPTool - Individual tool definitions")
    print(f"  • MCPRegistry - Server management and routing")
    print(f"  • MCPClient - High-level tool calling interface")
    print(f"")
    print(f"Available commands:")
    print(f"  demo basic    - Run basic calculator demo")
    print(f"  demo multi    - Run multi-server workflow demo")
    print(f"  test          - Run test suite")
    print(f"  info          - Show this information")

def run_tests():
    """Run the test suite"""
    import subprocess
    
    tests_dir = os.path.join(os.path.dirname(__file__), '..', 'tests')
    
    if not os.path.exists(tests_dir):
        print(f"❌ Tests directory not found: {tests_dir}")
        return 1
    
    print(f"🧪 Running MCP Tools test suite...")
    
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pytest', tests_dir, '-v'
        ], cwd=os.path.dirname(tests_dir))
        
        return result.returncode
        
    except FileNotFoundError:
        # Fallback to unittest if pytest not available
        print("📝 pytest not found, using unittest...")
        
        try:
            result = subprocess.run([
                sys.executable, '-m', 'unittest', 'discover', '-s', tests_dir, '-v'
            ], cwd=os.path.dirname(tests_dir))
            
            return result.returncode
            
        except Exception as e:
            print(f"❌ Test execution failed: {e}")
            return 1

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="MCP Tools - Model Context Protocol Framework CLI",
        prog="mcp-tools"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Demo command
    demo_parser = subparsers.add_parser('demo', help='Run demo applications')
    demo_parser.add_argument('name', choices=['basic', 'multi'], 
                            help='Demo to run')
    
    # Test command
    subparsers.add_parser('test', help='Run test suite')
    
    # Info command
    subparsers.add_parser('info', help='Show framework information')
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    # Execute commands
    if args.command == 'demo':
        return run_demo(args.name)
    elif args.command == 'test':
        return run_tests()
    elif args.command == 'info':
        show_info()
        return 0
    else:
        parser.print_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())