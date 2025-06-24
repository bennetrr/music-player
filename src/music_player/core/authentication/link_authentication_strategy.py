__all__ = ['LinkAuthenticationStrategy']

from music_player.core.authentication import AuthenticationStrategy


class LinkAuthenticationStrategy(AuthenticationStrategy):
    """
    An authentication strategy where the user needs to visit a website.

    :var link: The link to the website.
    """

    link: str
