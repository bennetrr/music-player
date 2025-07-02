__all__ = ['Provider']

from abc import ABC, abstractmethod

from music_player.core.authentication import AuthenticationResult
from music_player.core.music.models import Playable, PlayableContainer, SearchResult, Track
from music_player.core.plugin_manager import BasePlugin, PluginContext


class Provider(BasePlugin, ABC):
    """
    A provider is responsible for accessing a music library from a service.

    A provider handles:

    - Authentication to the service
    - Searching for and listing content
    - Resolving a track to a playable URI
    - Getting metadata for a track
    """

    def __init__(self, context: PluginContext) -> None:
        """Initialize the provider."""
        super().__init__(context)

    def close(self) -> None:
        """Clean up resources."""

    @property
    @abstractmethod
    def id(self) -> str:
        """A unique ID of the music provider instance."""

    @abstractmethod
    async def login(self) -> AuthenticationResult:
        """Log in to the service."""

    @abstractmethod
    async def search(self, query: str) -> SearchResult:
        """Search the provider's library."""

    @abstractmethod
    async def list(self, arg: PlayableContainer) -> SearchResult:
        """List the content in the provider's library."""

    @abstractmethod
    async def resolve_uri(self, track: Playable) -> str:
        """Resolve a track to a playable URI."""

    @abstractmethod
    async def get_metadata(self, track: Playable) -> Track:
        """Get the metadata for a track."""
