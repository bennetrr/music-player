__all__ = ['LinkAuthenticationStrategy']

from .authentication_strategy import AuthenticationStrategy


class LinkAuthenticationStrategy(AuthenticationStrategy):
    """
    An authentication strategy where the user needs to visit a website.

    :var link: The link to the website.
    """

    link: str

    def __str__(self) -> str:
        return f'Open {self.link} in your browser. The link will expire at {self.expires}'
