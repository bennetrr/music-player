from asyncio import Task

from pydantic import BaseModel, ConfigDict, Field

from .authentication_strategy import AuthenticationStrategy


class AuthenticationResult(BaseModel):
    """
    The result of an authentication attempt.

    If credentials are already present in the credential store, ``result`` is a boolean.
    Otherwise, it is a future that will be resolved when authentication is complete.

    ``strategies`` contains the authentication strategies the user can use.
    It is empty if no user interaction is required, e.g., if credentials are already present.

    :var result: The result of the authentication attempt.
    :var strategies: The authentication strategies if applicable.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    result: bool | Task[bool]
    strategies: list[AuthenticationStrategy] = Field(default_factory=list)
