"""Build a knowledge tree from summarized documents."""

from __future__ import annotations

import json
import logging

from isabl_knowledge.llm import get_client, get_default_model
from isabl_knowledge.models import Document, TreeNode

logger = logging.getLogger(__name__)

TREE_PROMPT = """You are organizing documentation for the Isabl genomics platform into a navigable knowledge tree.

Given these {count} documents (each with doc_id, title, summary, tags), create a DEEP hierarchical tree:

STRUCTURE REQUIREMENTS:
- Use 3-4 levels of depth (root → domain → area → topic → documents)
- Root should have 5-8 top-level domains
- Each domain should have 2-5 areas
- Areas with 8+ documents MUST be split into sub-topics
- Only leaf nodes list doc_ids — intermediate nodes have children only
- Max 100 total nodes
- Each node needs: id (dotted notation like "0001.0002.0003"), title, summary, and either children or documents (never both)

GROUPING GUIDELINES:
- Group by user intent and capabilities, not code structure
- Think: "What would a researcher/engineer search for?"
- Example levels: "Data Management" → "Importing Data" → "File Formats & Validation" → [doc_ids]

Documents:
{documents}

Return a JSON object representing the root TreeNode. No markdown fencing."""


def build_tree(docs: list[Document], model: str | None = None) -> TreeNode:
    """Build a knowledge tree from summarized documents."""
    client = get_client()
    model = model or get_default_model()

    doc_summaries = json.dumps([
        {"doc_id": d.doc_id, "title": d.title, "summary": d.summary, "tags": d.tags}
        for d in docs
    ], indent=2)

    prompt = TREE_PROMPT.format(count=len(docs), documents=doc_summaries)

    response = client.chat.completions.create(
        model=model,
        max_completion_tokens=32768,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.choices[0].message.content or ""
    # Strip markdown fencing if present
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()

    if not text:
        raise ValueError(
            f"LLM returned empty response. "
            f"Finish reason: {response.choices[0].finish_reason}, "
            f"Usage: {response.usage}"
        )

    data = json.loads(text)
    return TreeNode(**data)
