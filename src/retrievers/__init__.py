"""
Retriever package for handling various retriever architectures.

This package provides a modular, extensible system for using different
retriever types.
"""

import logging
import asyncio

from .base import BaseRetriever
from .kg_lightrag import KGLightRAG


class RetrieverRegistry:
    """
    Registry for managing retrievers.
    """

    def __init__(self):
        self._retrievers: list[BaseRetriever] = []
        self._register_default_retrievers()

    def _register_default_retrievers(self):
        """Register all default retrievers."""
        default_retrievers = [
            KGLightRAG(),
        ]

        for retriever in default_retrievers:
            self.register_retriever(retriever)

    def register_retriever(self, retriever: BaseRetriever):
        self._retrievers.append(retriever)

    def get_all_retrievers(self) -> list[BaseRetriever]:
        """
        Get all registered processors.

        Returns
        -------
        Dict[str, BaseFileProcessor]
            Dictionary mapping processor names to processor instances
        """
        return self._retrievers.copy()


# Global processor registry instance
_retriever_registry = RetrieverRegistry()


def get_retriever_registry() -> RetrieverRegistry:
    """
    Get the global processor registry instance.

    Returns
    -------
    ProcessorRegistry
        The global processor registry
    """
    return _retriever_registry


class HybridRetriever:
    """
    Main retriever class that coordinates with the retriever registry.

    This class provides the main interface for retrieving.
    """

    def __init__(self, retriever_registry: RetrieverRegistry = None):
        """
        Initialize the FileProcessor.

        Parameters
        ----------
        processor_registry : ProcessorRegistry, optional
            Custom processor registry. If None, uses the global registry.
        """
        self.registry = retriever_registry or get_retriever_registry()

    def index(self, directory: str) -> None:
        """
        Process a directory of files and index all content to retrievers.
        """

        retrievers = self.registry.get_all_retrievers()
        if not retrievers:
            raise Exception(f"No retrievers registered")

        for retriever in retrievers:
            asyncio.run(retriever.aindex(directory))


# Export main classes and functions
__all__ = [
    'BaseRetriever',
    'RetrieverRegistry',
    'HybridRetriever',
    'get_retriever_registry',
    'KGLightRAGRetriever',
]