__all__ = ['NotPlayingError']


class NotPlayingError(Exception):
    """Raised when the player is not playing, but the operation requires it to play."""
