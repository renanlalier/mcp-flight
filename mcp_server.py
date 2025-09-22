#!/usr/bin/env python3
"""
MCP Flight Server - Main entry point
"""
import sys
import os
import logging
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Add src to Python path
src_dir = Path(__file__).parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# Configure PYTHONPATH
os.environ["PYTHONPATH"] = str(src_dir) + ":" + os.environ.get("PYTHONPATH", "")

# Import presentation modules (after configuring sys.path)
from src.presentation.mcp.tools import register_tools  
from src.presentation.mcp.prompts import register_prompts
from src.presentation.mcp.resources import register_resources

def main():
    """Runs the MCP server"""
    
    # Configure logging
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stderr
    )
    
    # Initialize MCP server
    mcp = FastMCP("flight")
    
    # Register components
    register_tools(mcp)
    register_prompts(mcp)
    register_resources(mcp)
    
    # Run server
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
