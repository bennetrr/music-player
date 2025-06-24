__all__ = ['AlreadyPlayingError']


class AlreadyPlayingError(Exception):
    """Raised when trying to play a track while another is already playing."""
