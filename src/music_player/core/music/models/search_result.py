__all__ = ['SearchResult']

from pydantic import BaseModel, Field

from .album import Album
from .artist import Artist
from .playlist import Playlist
from .radio import Radio
from .track import Track


class SearchResult(BaseModel):
    """Search results."""

    artists: list[Artist] = Field(default_factory=list)
    albums: list[Album] = Field(default_factory=list)
    playlists: list[Playlist] = Field(default_factory=list)
    songs: list[Track] = Field(default_factory=list)
    podcasts: list[Track] = Field(default_factory=list)
    radios: list[Radio] = Field(default_factory=list)
