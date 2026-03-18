"""Tests for the LLM summarizer."""

from unittest.mock import patch, MagicMock

import pytest

from isabl_knowledge.models import Document
from isabl_knowledge.summarizer import summarize_document, summarize_documents


@pytest.fixture
def sample_doc():
    return Document(
        doc_id="cli/get_experiments",
        source_type="github_docstring",
        source_url="https://github.com/test/repo",
        content="# get_experiments\n\nQuery experiments from Isabl by project, technique, or status.",
    )


def test_summarize_document_calls_llm(sample_doc):
    """Test that summarize_document returns a document with title, summary, tags, questions."""
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="""{
        "title": "Query Experiments from Isabl",
        "summary": "Function to retrieve experiments filtered by project, technique, or status.",
        "tags": ["experiments", "querying", "SDK"],
        "questions": ["How do I get experiments for a project?"]
    }""")]

    with patch("isabl_knowledge.summarizer.get_client") as mock_client:
        mock_client.return_value.messages.create.return_value = mock_response
        result = summarize_document(sample_doc)

    assert result.title == "Query Experiments from Isabl"
    assert result.summary != ""
    assert len(result.tags) > 0
    assert len(result.questions) > 0
    assert result.doc_id == sample_doc.doc_id
    assert result.content == sample_doc.content


def test_summarize_document_handles_json_error(sample_doc):
    """Test that summarize_document handles malformed JSON gracefully."""
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="not valid json")]

    with patch("isabl_knowledge.summarizer.get_client") as mock_client:
        mock_client.return_value.messages.create.return_value = mock_response
        result = summarize_document(sample_doc)

    # Should return the original doc unchanged
    assert result.title == ""
    assert result.summary == ""
    assert result.tags == []
    assert result.questions == []


def test_summarize_documents_processes_all(sample_doc):
    """Test that summarize_documents processes every document in the list."""
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="""{
        "title": "Test Title",
        "summary": "Test summary.",
        "tags": ["test"],
        "questions": ["What is this?"]
    }""")]

    docs = [sample_doc, sample_doc.model_copy(update={"doc_id": "cli/get_analyses"})]

    with patch("isabl_knowledge.summarizer.get_client") as mock_client:
        mock_client.return_value.messages.create.return_value = mock_response
        results = summarize_documents(docs)

    assert len(results) == 2
    assert results[0].title == "Test Title"
    assert results[1].title == "Test Title"
