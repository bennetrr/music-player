__all__ = ['PositionOutOfBoundsError']


class PositionOutOfBoundsError(ValueError):
    """Raised when trying to set the playback position outside the bounds of the currently playing item."""

    def __init__(self, max_value: float, value: float) -> None:
        """Initialize the error."""
        super().__init__(
            f'The specified playback position is out of bounds for the currently playing item'
            f' (expected a value between 0 s and {max_value} s, got {value} s).'
        )
