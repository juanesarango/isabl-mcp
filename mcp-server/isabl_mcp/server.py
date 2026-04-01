"""Isabl MCP Server - Main entry point.

This MCP server provides AI agents access to the Isabl genomics platform.

Tools provided:
- isabl_query: Query any API endpoint
- isabl_get_tree: Get individual hierarchy
- isabl_get_results: Get analysis results
- isabl_get_logs: Get analysis logs
- get_apps: Search and get details for applications
- get_app_template: Get app boilerplate code
- merge_results: Combine results from multiple analyses
- project_summary: Get project statistics
- search_knowledge: Search the Isabl knowledge base
- get_knowledge_tree: Browse the knowledge tree hierarchy
- get_knowledge_doc: Get full content of a knowledge document

Usage:
    isabl-mcp
    python -m isabl_mcp.server
    uvx isabl-mcp

Environment variables:
    ISABL_API_URL: Isabl API URL (default: http://localhost:8000/api/v1/)
    ISABL_API_TOKEN: API authentication token
"""

import logging

from mcp.server.fastmcp import FastMCP

from isabl_mcp.config import settings
from isabl_mcp.clients.isabl_api import IsablAPIClient
from isabl_mcp.tools.data import register_data_tools
from isabl_mcp.tools.apps import register_app_tools
from isabl_mcp.tools.aggregation import register_aggregation_tools
from isabl_mcp.tools.knowledge import register_knowledge_tools
from isabl_mcp.prompts import register_prompts


# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_server() -> FastMCP:
    """Create and configure the MCP server."""
    # Initialize FastMCP server
    mcp = FastMCP("Isabl MCP Server")

    # Initialize Isabl API client
    api_client = IsablAPIClient()

    # Register API tools
    logger.info("Registering data tools...")
    register_data_tools(mcp, api_client)

    logger.info("Registering app tools...")
    register_app_tools(mcp, api_client)

    logger.info("Registering aggregation tools...")
    register_aggregation_tools(mcp, api_client)

    # Register knowledge base tools (uses bundled data)
    logger.info("Registering knowledge tools...")
    register_knowledge_tools(mcp)

    # Register prompts (guided workflows)
    logger.info("Registering prompts...")
    register_prompts(mcp)

    logger.info(
        f"Isabl MCP Server initialized. API URL: {settings.isabl_api_url}"
    )

    return mcp


# Create the server instance
mcp = create_server()


def main():
    """Entry point for the MCP server."""
    logger.info("Starting Isabl MCP Server...")
    mcp.run()


if __name__ == "__main__":
    main()
