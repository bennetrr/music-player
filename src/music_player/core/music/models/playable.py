__all__ = ['Playable']

from abc import ABC

from pydantic import BaseModel


class Playable(BaseModel, ABC):
    """
    A playable item, e.g., a track or radio station.

    :var provider_id: The ID of the provider where this playable comes from.
    :var id: A provider-dependent identifier for this playable.
    """

    provider_id: str
    id: str
