__all__ = ['AlreadyPlayingError']


class AlreadyPlayingError(Exception):
    """Raised when trying to start playback, but the player is already playing."""
