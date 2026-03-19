"""Render a knowledge tree as a Mermaid mindmap."""

from __future__ import annotations

from isabl_knowledge.models import TreeNode


def render_tree_to_mermaid(tree: TreeNode) -> str:
    """Render tree as a Mermaid mindmap diagram."""
    lines = ["```mermaid", "mindmap", f"  root(({tree.title}))"]
    for child in tree.children:
        _render_node(child, lines, depth=2)
    lines.append("```")
    return "\n".join(lines)


def _render_node(node: TreeNode, lines: list[str], depth: int) -> None:
    """Recursively render tree nodes as mindmap entries."""
    indent = "  " * depth
    doc_count = len(node.documents)
    if doc_count:
        lines.append(f"{indent}{node.title} [{doc_count}]")
    else:
        lines.append(f"{indent}{node.title}")
    for child in node.children:
        _render_node(child, lines, depth + 1)
