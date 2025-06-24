__all__ = ['RepeatMode']

from enum import StrEnum


class RepeatMode(StrEnum):
    """Repeat mode."""

    OFF = 'off'
    ONE = 'one'
    ALL = 'all'
