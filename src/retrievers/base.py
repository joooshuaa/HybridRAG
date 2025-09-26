from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class BaseRetriever(ABC):

    @property
    @abstractmethod
    def retriever_name(self) -> str:
        """
        Return a human-readable name for this processor.
        
        Returns
        -------
        str
            Name of the processor (e.g., "PDF Processor")
        """
        pass

    @abstractmethod
    def index(self, directory: str) -> None:
        """
        Index text content from the given file bytes.
        
        Parameters
        ----------
        directory : str
            Where to find the to be indexed files
            
        Returns
        -------
        None
            
        Raises
        ------
        ValueError
            If the file cannot be processed or is corrupted
        """
        pass

    @abstractmethod
    async def aindex(self, directory: str) -> None:
        """
        Index text content from the given file bytes.

        Parameters
        ----------
        directory : str
            Where to find the to be indexed files

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the file cannot be processed or is corrupted
        """
        pass

    @abstractmethod
    def retrieve(self, file_content: bytes, filename: str, content_type: str = None) -> str:
        pass

    def __str__(self) -> str:
        """String representation of the processor."""
        return f"{self.retriever_name}"