__all__ = ['SearchResult']

from pydantic import BaseModel, Field

from music_player.core.music import Album, Artist, Playlist, Track


class SearchResult(BaseModel):
    """Search results."""

    artists: list[Artist] = Field(default_factory=list)
    albums: list[Album] = Field(default_factory=list)
    playlists: list[Playlist] = Field(default_factory=list)
    songs: list[Track] = Field(default_factory=list)
    podcasts: list[Track] = Field(default_factory=list)
    radios: list[Track] = Field(default_factory=list)
