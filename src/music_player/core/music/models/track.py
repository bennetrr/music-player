__all__ = ['Track']

from pydantic import BaseModel

from music_player.core.music.enums import TrackType


class Track(BaseModel):
    """
    A playable item, e.g., a song, podcast, or radio station.

    :var type: The type of track. This specifies if the track is an endless stream or not.
    :var provider_id: The ID of the provider where this track comes from.
    :var id: A provider-dependent identifier for this track.
    """

    type: TrackType
    provider_id: str
    id: str
