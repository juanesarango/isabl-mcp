"""Registry mapping source types to extractor classes."""

from __future__ import annotations

from isabl_knowledge.config import SourceConfig
from isabl_knowledge.extractors.base import BaseExtractor
from isabl_knowledge.extractors.django_api import DjangoAPIExtractor
from isabl_knowledge.extractors.gitbook import GitbookExtractor
from isabl_knowledge.extractors.github_python import PythonExtractor
from isabl_knowledge.extractors.openapi import OpenAPIExtractor


EXTRACTORS: dict[str, type[BaseExtractor]] = {
    "github_python": PythonExtractor,
    "gitbook": GitbookExtractor,
    "openapi": OpenAPIExtractor,
    "django_api": DjangoAPIExtractor,
}


def get_extractor(source: SourceConfig) -> BaseExtractor:
    """Get the appropriate extractor for a source config."""
    cls = EXTRACTORS.get(source.type)
    if cls is None:
        raise ValueError(f"Unknown source type: {source.type}. Available: {list(EXTRACTORS.keys())}")
    return cls(source)
