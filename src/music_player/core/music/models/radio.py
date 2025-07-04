__all__ = ['Radio']


from .playable import Playable


class Radio(Playable):
    """
    A radio.

    :var title: The title of the radio.
    :var cover_uri: The URL of the cover image for the radio.
    """

    title: str
    cover_uri: str | None
