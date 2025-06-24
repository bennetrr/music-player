__all__ = ['Provider']

from abc import ABC, abstractmethod


class Provider(ABC):
    @abstractmethod
    @property
    def id(self) -> str:
        """A unique ID of the music provider instance."""
