__all__ = ['TrackContainer']

from abc import ABC

from pydantic import BaseModel, field_serializer, field_validator

from music_player.core.music import Provider


class TrackContainer(BaseModel, ABC):
    """
    Something that contains tracks, like a playlist or album.

    :var provider: The provider instance where this track container comes from.
    :var id: A provider-dependent identifier for this track container.
    """

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
