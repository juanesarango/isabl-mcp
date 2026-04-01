"""Tests for knowledge tree tools."""

import json
import pytest
from pathlib import Path
from unittest.mock import patch

from isabl_mcp.tools.knowledge import KnowledgeIndex, register_knowledge_tools


# Sample test data
SAMPLE_TREE = {
    "id": "0001",
    "title": "Isabl Knowledge Tree",
    "summary": "Root of the knowledge tree",
    "children": [
        {
            "id": "0001.0001",
            "title": "Getting Started",
            "summary": "Introductory documentation",
            "children": [
                {
                    "id": "0001.0001.0001",
                    "title": "Quick Start",
                    "summary": "Quick start guide",
                    "children": [],
                    "documents": ["docs/quick-start"],
                }
            ],
            "documents": [],
        },
        {
            "id": "0001.0002",
            "title": "Applications",
            "summary": "Application development guides",
            "children": [],
            "documents": ["cli/AbstractApplication", "docs/writing-apps"],
        },
    ],
}

SAMPLE_DOCS = [
    {
        "doc_id": "docs/quick-start",
        "source_type": "gitbook",
        "source_url": "https://docs.isabl.io/quick-start",
        "title": "Quick Start Guide",
        "summary": "Get started with Isabl in 5 minutes",
        "tags": ["getting-started", "tutorial"],
        "questions": ["How do I install Isabl?"],
        "content": "Welcome to Isabl. Install with pip install isabl_cli.",
        "metadata": {},
    },
    {
        "doc_id": "cli/AbstractApplication",
        "source_type": "github_python",
        "source_url": "https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py",
        "title": "AbstractApplication",
        "summary": "Base class for all Isabl applications",
        "tags": ["application", "pipeline", "base-class"],
        "questions": ["How do I write an Isabl application?"],
        "content": "class AbstractApplication: ...",
        "metadata": {},
    },
    {
        "doc_id": "docs/writing-apps",
        "source_type": "gitbook",
        "source_url": "https://docs.isabl.io/writing-apps",
        "title": "Writing Applications",
        "summary": "Guide to writing custom Isabl applications",
        "tags": ["application", "development", "tutorial"],
        "questions": ["What methods do I need to implement?"],
        "content": "To write an application, extend AbstractApplication and implement get_command.",
        "metadata": {},
    },
]


@pytest.fixture
def knowledge_data(tmp_path):
    """Create temporary knowledge data files."""
    tree_path = tmp_path / "tree.json"
    docs_path = tmp_path / "documents.json"
    tree_path.write_text(json.dumps(SAMPLE_TREE))
    docs_path.write_text(json.dumps(SAMPLE_DOCS))
    return tree_path, docs_path


@pytest.fixture
def index(knowledge_data):
    """Create a KnowledgeIndex from sample data."""
    tree_path, docs_path = knowledge_data
    return KnowledgeIndex(tree_path, docs_path)


class TestKnowledgeIndex:
    def test_loads_tree(self, index):
        assert index.tree_data["id"] == "0001"
        assert len(index.node_index) == 4  # root + 2 children + 1 grandchild

    def test_loads_docs(self, index):
        assert len(index.docs) == 3
        assert "docs/quick-start" in index.docs

    def test_search_by_title(self, index):
        results = index.search("Quick Start")
        assert len(results) > 0
        assert results[0]["doc_id"] == "docs/quick-start"

    def test_search_by_tag(self, index):
        results = index.search("application")
        assert len(results) >= 2
        doc_ids = [r["doc_id"] for r in results]
        assert "cli/AbstractApplication" in doc_ids
        assert "docs/writing-apps" in doc_ids

    def test_search_by_content(self, index):
        results = index.search("pip install")
        assert len(results) > 0
        assert results[0]["doc_id"] == "docs/quick-start"

    def test_search_no_results(self, index):
        results = index.search("xyznonexistent")
        assert len(results) == 0

    def test_search_limit(self, index):
        results = index.search("application", limit=1)
        assert len(results) == 1

    def test_search_returns_score(self, index):
        results = index.search("application")
        assert all("score" in r for r in results)
        # Results should be sorted by score descending
        scores = [r["score"] for r in results]
        assert scores == sorted(scores, reverse=True)


class TestKnowledgeTools:
    @pytest.fixture
    def mcp_with_knowledge(self, knowledge_data):
        """Create an MCP server with knowledge tools registered."""
        from mcp.server.fastmcp import FastMCP

        tree_path, docs_path = knowledge_data
        mcp = FastMCP("test")

        with patch("isabl_mcp.tools.knowledge.DATA_DIR", tree_path.parent):
            idx = register_knowledge_tools(mcp)

        return mcp, idx

    def test_register_returns_index(self, mcp_with_knowledge):
        _, idx = mcp_with_knowledge
        assert idx is not None
        assert len(idx.docs) == 3

    def test_register_missing_data(self, tmp_path):
        from mcp.server.fastmcp import FastMCP

        mcp = FastMCP("test")
        with patch("isabl_mcp.tools.knowledge.DATA_DIR", tmp_path):
            idx = register_knowledge_tools(mcp)
        assert idx is None

    @pytest.mark.asyncio
    async def test_search_knowledge_tool(self, mcp_with_knowledge):
        mcp, _ = mcp_with_knowledge
        # Access tool via the mcp's tool registry
        tools = mcp._tool_manager._tools
        search_tool = tools.get("search_knowledge")
        assert search_tool is not None

    @pytest.mark.asyncio
    async def test_get_knowledge_tree_tool(self, mcp_with_knowledge):
        mcp, _ = mcp_with_knowledge
        tools = mcp._tool_manager._tools
        tree_tool = tools.get("get_knowledge_tree")
        assert tree_tool is not None

    @pytest.mark.asyncio
    async def test_get_knowledge_doc_tool(self, mcp_with_knowledge):
        mcp, _ = mcp_with_knowledge
        tools = mcp._tool_manager._tools
        doc_tool = tools.get("get_knowledge_doc")
        assert doc_tool is not None
