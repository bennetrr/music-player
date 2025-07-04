__all__ = ['QueueOutOfBoundsError']


class QueueOutOfBoundsError(IndexError):
    """Raised when trying to access a queue item or index that is not in the queue."""
