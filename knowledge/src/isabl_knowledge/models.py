"""Data models for extracted documents and tree nodes."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Document(BaseModel):
    """An extracted document from any source."""

    doc_id: str
    source_type: str
    source_url: str
    content: str
    title: str = ""
    summary: str = ""
    tags: list[str] = Field(default_factory=list)
    questions: list[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)


class TreeNode(BaseModel):
    """A node in the knowledge tree."""

    id: str
    title: str
    summary: str = ""
    children: list[TreeNode] = Field(default_factory=list)
    documents: list[str] = Field(default_factory=list)
