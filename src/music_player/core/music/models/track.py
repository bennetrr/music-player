__all__ = ['Track']

from pydantic import BaseModel, field_serializer, field_validator

from music_player.core.music import Provider, TrackType


class Track(BaseModel):
    """
    A playable item, e.g., a song, podcast, or radio station.

    :var type: The type of track. This specifies if the track is an endless stream or not.
    :var provider: The provider instance where this track comes from.
    :var id: A provider-dependent identifier for this track.
    """

    type: TrackType
    provider: Provider
    id: str

    @field_serializer('provider')
    def serialize_provider(self, provider: Provider) -> str:
        """Serialize the provider instance to its ID."""
        return provider.id

    @classmethod
    @field_validator('provider')
    def validate_provider(cls, provider_id: str) -> None:
        """Deserialize the provider instance from its ID."""
        # TODO: Get the provider from the registry (#0)
