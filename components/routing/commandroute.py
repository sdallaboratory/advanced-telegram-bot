from typing import Callable, List

from .route import Route


class CommandRoute(Route):
    """
    Route serving incoming commands.

    ..........
    Attributes
    ----------
    command: str, public
        required incoming command to serve the route
    """
    def __init__(self,
                 command: str,
                 callback: Callable,
                 states: List[str],
                 roles: List[str]) -> None:
        """
        Constructor.

        .........
        Arguments
        ---------
        command: str, requited
            trigger command to serve the route
        callback: Callable, required
            function to be called when route is served
        states: List[str]
            states one of which user should have to access serving the route
        roles: List[str]
            roles one of which user should have to access serving the route
        """
        super().__init__(callback, states, roles)

        self.command = command
