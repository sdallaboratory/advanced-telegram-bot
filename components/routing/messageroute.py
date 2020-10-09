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
        """
        Constructor.

        .........
        Arguments
        ---------
        message: str, requited
            trigger regex message text to serve the route
        callback: Callable, required
            function to be called when route is served
        states: List[str]
            states one of which user should have to access serving the route
        roles: List[str]
            roles one of which user should have to access serving the route
        """
        super().__init__(callback, states, roles)

        self.message = message
