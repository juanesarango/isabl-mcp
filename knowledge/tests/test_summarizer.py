"""Tests for the LLM summarizer."""

import json
from unittest.mock import patch, AsyncMock, MagicMock

import pytest

from isabl_knowledge.models import Document
from isabl_knowledge.summarizer import summarize_documents, _parse_batch_response


@pytest.fixture
def sample_docs():
    return [
        Document(
            doc_id="cli/get_experiments",
            source_type="github_docstring",
            source_url="https://github.com/test/repo",
            content="# get_experiments\n\nQuery experiments from Isabl.",
        ),
        Document(
            doc_id="cli/get_analyses",
            source_type="github_docstring",
            source_url="https://github.com/test/repo",
            content="# get_analyses\n\nQuery analyses from Isabl.",
        ),
    ]


def _mock_async_response(content: str):
    """Create a mock async client that returns the given content."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content=content))]

    mock_client = AsyncMock()
    mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
    return mock_client


def test_summarize_documents_batch(sample_docs):
    """Test that summarize_documents processes a batch and returns summaries."""
    batch_response = json.dumps([
        {
            "doc_id": "cli/get_experiments",
            "title": "Query Experiments",
            "summary": "How to query experiments.",
            "tags": ["experiments"],
            "questions": ["How do I get experiments?"],
        },
        {
            "doc_id": "cli/get_analyses",
            "title": "Query Analyses",
            "summary": "How to query analyses.",
            "tags": ["analyses"],
            "questions": ["How do I get analyses?"],
        },
    ])

    with patch("isabl_knowledge.summarizer.get_async_client") as mock_get:
        mock_get.return_value = _mock_async_response(batch_response)
        results = summarize_documents(sample_docs)

    assert len(results) == 2
    assert results[0].title == "Query Experiments"
    assert results[1].title == "Query Analyses"
    assert results[0].doc_id == "cli/get_experiments"


def test_summarize_documents_skips_already_done(sample_docs):
    """Test that already-summarized documents are skipped."""
    sample_docs[0].summary = "Already done"
    sample_docs[0].title = "Already Done Title"

    batch_response = json.dumps([{
        "doc_id": "cli/get_analyses",
        "title": "Query Analyses",
        "summary": "How to query analyses.",
        "tags": ["analyses"],
        "questions": ["How do I get analyses?"],
    }])

    with patch("isabl_knowledge.summarizer.get_async_client") as mock_get:
        mock_client = _mock_async_response(batch_response)
        mock_get.return_value = mock_client
        results = summarize_documents(sample_docs)

    assert results[0].title == "Already Done Title"
    assert results[1].title == "Query Analyses"
    assert mock_client.chat.completions.create.call_count == 1


def test_parse_batch_response_handles_bad_json():
    """Test that malformed JSON is handled gracefully."""
    result = _parse_batch_response("not valid json", [])
    assert result == {}


def test_parse_batch_response_strips_markdown_fencing():
    """Test that markdown code fences are stripped before parsing."""
    text = '```json\n[{"doc_id": "test", "title": "Test"}]\n```'
    result = _parse_batch_response(text, [])
    assert "test" in result
    assert result["test"]["title"] == "Test"
