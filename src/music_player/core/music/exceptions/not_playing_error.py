__all__ = ['NotPlayingError']


class NotPlayingError(Exception):
    """Raised when no track is playing, but the operation requires one to play."""
