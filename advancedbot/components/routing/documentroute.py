from typing import Callable, List

from .route import Route


class DocumentRoute(Route):
    """
    Route serving incoming documents.

    ..........
    Attributes
    ----------
    filenames: List[str], public
        required names of incoming files to serve the route
    mime_types: List[str], public
        required MIME-types of incoming files to serve the route
    """
    def __init__(self,
                 callback: Callable,
                 states: List[str],
                 roles: List[str],
                 filenames: List[str],
                 mime_types: List[str]) -> None:
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
            filenames one of which incoming file should have to serve the route
            if empty, every filename is valid
        mime_types: List[str], required
            MIME-types one of which incoming file should have to serve the route
            if empty, every MIME-type is valid
        """
        super().__init__(callback, states, roles)

        self.filenames = filenames
        self.mime_types = mime_types

