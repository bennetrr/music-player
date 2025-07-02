__all__ = ['Artist']


from .playable_container import PlayableContainer


class Artist(PlayableContainer):
    """An artist."""

    name: str
    cover_uri: str | None
