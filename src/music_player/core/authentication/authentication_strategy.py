__all__ = ['AuthenticationStrategy']

from abc import ABC

from pydantic import BaseModel, FutureDatetime


class AuthenticationStrategy(BaseModel, ABC):
    """
    An authentication strategy defines the way a user authenticates with a music provider.

    The most common strategies are authentication via a link or a code.

    :var expires: The time when the authentication gets invalidated.
    """

    expires: FutureDatetime
