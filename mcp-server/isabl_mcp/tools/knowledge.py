"""Knowledge tree tools for Isabl MCP Server.

Tools:
- search_knowledge: Search Isabl documentation and knowledge base
- get_knowledge_tree: Browse the knowledge tree hierarchy
- get_knowledge_doc: Get full content of a knowledge document
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)

# Data directory bundled with the package
DATA_DIR = Path(__file__).parent.parent / "data"


class KnowledgeIndex:
    """In-memory index over the knowledge tree and documents."""

    def __init__(self, tree_path: Path, docs_path: Path):
        self.tree_data = json.loads(tree_path.read_text())
        docs_list = json.loads(docs_path.read_text())
        self.docs: Dict[str, dict] = {d["doc_id"]: d for d in docs_list}
        self.node_index: Dict[str, dict] = {}
        self._index_nodes(self.tree_data)

    def _index_nodes(self, node: dict) -> None:
        """Recursively index all tree nodes by ID."""
        self.node_index[node["id"]] = node
        for child in node.get("children", []):
            self._index_nodes(child)

    def search(self, query: str, limit: int = 10) -> List[dict]:
        """Search documents by keyword matching across title, summary, tags, and content."""
        query_lower = query.lower()
        terms = query_lower.split()
        scored: List[tuple[float, dict]] = []

        for doc in self.docs.values():
            score = 0.0
            title = (doc.get("title") or "").lower()
            summary = (doc.get("summary") or "").lower()
            tags = [t.lower() for t in doc.get("tags", [])]
            questions = [q.lower() for q in doc.get("questions", [])]
            content = (doc.get("content") or "").lower()

            for term in terms:
                # Title match (highest weight)
                if term in title:
                    score += 10.0
                # Tag match
                if any(term in t for t in tags):
                    score += 5.0
                # Question match
                if any(term in q for q in questions):
                    score += 4.0
                # Summary match
                if term in summary:
                    score += 3.0
                # Content match
                if term in content:
                    score += 1.0

            if score > 0:
                scored.append((score, doc))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [
            {
                "doc_id": doc["doc_id"],
                "title": doc.get("title", ""),
                "summary": doc.get("summary", ""),
                "tags": doc.get("tags", []),
                "source_url": doc.get("source_url", ""),
                "score": round(score, 1),
            }
            for score, doc in scored[:limit]
        ]


def register_knowledge_tools(mcp: FastMCP) -> Optional[KnowledgeIndex]:
    """Register knowledge tree tools with the MCP server.

    Returns the KnowledgeIndex if data files are found, None otherwise.
    """
    tree_path = DATA_DIR / "tree.json"
    docs_path = DATA_DIR / "documents.json"

    if not tree_path.exists() or not docs_path.exists():
        logger.warning("Knowledge data not found at %s, skipping knowledge tools", DATA_DIR)
        return None

    index = KnowledgeIndex(tree_path, docs_path)
    logger.info("Loaded knowledge tree: %d nodes, %d documents", len(index.node_index), len(index.docs))

    @mcp.tool()
    async def search_knowledge(
        query: str,
        limit: int = 10,
    ) -> Dict[str, Any]:
        """
        Search the Isabl knowledge base for documentation, code patterns, and API references.

        Searches across 289+ documents extracted from Isabl's source code, documentation,
        and API specifications. Matches against titles, summaries, tags, and content.

        Args:
            query: Search terms (e.g., "write application", "experiment query", "tumor normal")
            limit: Maximum number of results to return (default 10)

        Returns:
            List of matching documents with title, summary, tags, and relevance score

        Examples:
            search_knowledge("how to write an application")
            search_knowledge("variant calling pipeline")
            search_knowledge("experiment query filter")
        """
        results = index.search(query, limit=limit)
        return {
            "query": query,
            "count": len(results),
            "results": results,
        }

    @mcp.tool()
    async def get_knowledge_tree(
        node_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Browse the Isabl knowledge tree hierarchy.

        The knowledge tree organizes all Isabl documentation into a navigable hierarchy.
        Call without arguments to get the top-level categories, or pass a node_id to
        drill into a specific branch.

        Args:
            node_id: Optional node ID to get details for (e.g., "0001.0001").
                    If not provided, returns the top-level tree structure.

        Returns:
            Node details with children and/or linked documents

        Examples:
            get_knowledge_tree()                    # Top-level categories
            get_knowledge_tree("0001.0001")         # Drill into a branch
        """
        if node_id is None:
            tree = index.tree_data
            return {
                "id": tree["id"],
                "title": tree["title"],
                "summary": tree["summary"],
                "children": [
                    {"id": c["id"], "title": c["title"], "summary": c.get("summary", "")}
                    for c in tree.get("children", [])
                ],
            }

        node = index.node_index.get(node_id)
        if not node:
            return {"error": f"Node '{node_id}' not found"}

        result: Dict[str, Any] = {
            "id": node["id"],
            "title": node["title"],
            "summary": node.get("summary", ""),
        }

        if node.get("children"):
            result["children"] = [
                {"id": c["id"], "title": c["title"], "summary": c.get("summary", "")}
                for c in node["children"]
            ]

        if node.get("documents"):
            result["documents"] = []
            for doc_id in node["documents"]:
                doc = index.docs.get(doc_id)
                if doc:
                    result["documents"].append({
                        "doc_id": doc["doc_id"],
                        "title": doc.get("title", ""),
                        "summary": doc.get("summary", ""),
                        "tags": doc.get("tags", []),
                    })

        return result

    @mcp.tool()
    async def get_knowledge_doc(doc_id: str) -> Dict[str, Any]:
        """
        Get the full content of a knowledge base document.

        Returns the complete document including source code, documentation text,
        or API specification content.

        Args:
            doc_id: Document ID (e.g., "cli/get_experiments", "docs/data-model",
                   "api/ExperimentSerializer")

        Returns:
            Full document with title, content, summary, tags, and source URL

        Example:
            get_knowledge_doc("cli/get_experiments")
            get_knowledge_doc("docs/data-model")
        """
        doc = index.docs.get(doc_id)
        if not doc:
            return {"error": f"Document '{doc_id}' not found"}
        return {
            "doc_id": doc["doc_id"],
            "title": doc.get("title", ""),
            "summary": doc.get("summary", ""),
            "tags": doc.get("tags", []),
            "questions": doc.get("questions", []),
            "source_url": doc.get("source_url", ""),
            "source_type": doc.get("source_type", ""),
            "content": doc.get("content", ""),
        }

    return index
