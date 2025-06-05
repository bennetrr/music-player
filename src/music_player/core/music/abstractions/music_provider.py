__all__ = ['MusicProvider']

from abc import ABC, abstractmethod


class MusicProvider(ABC):
    @abstractmethod
    @property
    def id(self) -> str:
        """A unique ID of the music provider instance."""
