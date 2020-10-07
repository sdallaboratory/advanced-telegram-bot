from typing import Callable, List

from .route import Route


class MessageRoute(Route):
    """
    Route serving incoming text messages.

    ..........
    Attributes
    ----------
    message: str, public
        regex string required to match with
        incoming text to serve the route
    """
    def __init__(self,
                 message: str,
                 callback: Callable,
                 states: List[str],
                 roles: List[str]) -> None:
        super().__init__(callback, states, roles)

        self.message = message
