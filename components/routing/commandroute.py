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
        super().__init__(callback, states, roles)

        self.command = command
