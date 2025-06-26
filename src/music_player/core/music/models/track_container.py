__all__ = ['TrackContainer']

from abc import ABC

from pydantic import BaseModel


class TrackContainer(BaseModel, ABC):
    """
    Something that contains tracks, like a playlist or album.

    :var provider_id: The ID of the provider where this track container comes from.
    :var id: A provider-dependent identifier for this track container.
    """

    provider_id: str
    id: str
