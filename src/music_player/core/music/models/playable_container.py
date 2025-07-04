__all__ = ['PlayableContainer']

from abc import ABC

from pydantic import BaseModel


class PlayableContainer(BaseModel, ABC):
    """
    Something that contains playable objects, e.g., a playlist or album.

    :var provider_id: The ID of the provider where this playable container comes from.
    :var id: A provider-dependent identifier for this playable container.
    """

    provider_id: str
    id: str
