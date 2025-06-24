__all__ = ['CodeAuthenticationStrategy']

from music_player.core.authentication import AuthenticationStrategy


class CodeAuthenticationStrategy(AuthenticationStrategy):
    """
    An authentication strategy where the user needs to enter a code on a website.

    :var code: The code the user needs to enter.
    :var link: The link to the website where the user needs to enter the code.
    """

    code: str
    link: str
