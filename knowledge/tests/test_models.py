"""Tests for document models."""

from isabl_knowledge.models import Document


def test_document_creation():
    doc = Document(
        doc_id="cli/get_experiments",
        source_type="github_docstring",
        source_url="https://github.com/isabl-io/isabl_cli",
        content="# get_experiments\n\nQuery experiments from Isabl.",
    )
    assert doc.doc_id == "cli/get_experiments"
    assert doc.title == ""
    assert doc.tags == []
    assert doc.summary == ""


def test_document_with_metadata():
    doc = Document(
        doc_id="api/experiments",
        source_type="openapi",
        source_url="https://github.com/isabl-io/isabl_api",
        content="GET /api/v1/experiments/",
        metadata={"method": "GET", "path": "/api/v1/experiments/"},
    )
    assert doc.metadata["method"] == "GET"
