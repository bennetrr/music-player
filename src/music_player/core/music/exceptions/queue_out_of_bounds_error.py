"""Raised when trying to access a track or queue index that is not in the queue."""

__all__ = ['QueueOutOfBoundsError']


class QueueOutOfBoundsError(IndexError):
    """Raised when trying to access a track or queue index that is not in the queue."""
