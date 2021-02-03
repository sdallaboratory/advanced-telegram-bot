from typing import Callable, List

from .route import Route


class ImageRoute(Route):
    """
    Route serving incoming images.

    ..........
    Attributes
    ----------
    filenames: List[str], public
        required names of incoming images to serve the route
    """
    def __init__(self,
                 callback: Callable,
                 states: List[str],
                 roles: List[str],
                 filenames: List[str]) -> None
        """
        Constructor.

        .........
        Arguments
        ---------
        callback: Callable, required
            function to be called when route is served
        states: List[str], required
            states one of which user should have to access serving the route
        roles: List[str], required
            roles one of which user should have to access serving the route
        filenames: List[str], required
            filenames one of which incoming images should have to serve the route
            if empty, every filename is valid
        """
        super().__init__(callback, states, roles)

        self.filenames = filenames

