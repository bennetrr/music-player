__all__ = ['Track']

from typing import Literal

from pydantic import BaseModel, field_serializer, field_validator

from music_player.core.music.abstractions import MusicProvider


class Track(BaseModel):
    """A playable item, e.g., a track or a radio station."""

    type: Literal['track', 'radio']
    provider: MusicProvider
    id: str

    @field_serializer('provider')
    def serialize_provider(self, value: MusicProvider) -> str:
        return value.id

    @field_validator('provider')
    def validate_provider(cls, value: str) -> MusicProvider:
        return NotImplemented
