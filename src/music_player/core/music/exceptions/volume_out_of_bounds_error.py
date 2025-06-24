__all__ = ['VolumeOutOfBoundsError']


class VolumeOutOfBoundsError(ValueError):
    """Raised when trying to set the volume outside the bounds of 0 % and 100 %."""

    def __init__(self, value: float) -> None:
        """Initialize the error."""
        super().__init__(
            f'The specified volume is out of bounds (expected a value between 0 % and 100 %, got {value} %).'
        )
