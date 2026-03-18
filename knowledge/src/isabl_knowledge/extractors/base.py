"""Base class for source extractors."""

from __future__ import annotations

import abc

from isabl_knowledge.config import SourceConfig
from isabl_knowledge.models import Document


class BaseExtractor(abc.ABC):
    """Base class for extracting documents from a source."""

    def __init__(self, source: SourceConfig):
        self.source = source

    @abc.abstractmethod
    def extract(self) -> list[Document]:
        """Extract documents from the source. Returns a list of Documents."""
        ...
