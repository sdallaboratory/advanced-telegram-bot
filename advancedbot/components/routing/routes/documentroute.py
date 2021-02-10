from typing import Callable, List

from .route import Route


class DocumentRoute(Route):
    """
    Route serving incoming documents.

    ..........
    Attributes
    ----------
    file_names: List[str], public
        required names of incoming files to serve the route
    mime_types: List[str], public
        required MIME-types of incoming files to serve the route
    """
    def __init__(self,
                 file_names: List[str],
                 mime_types: List[str],
                 callback: Callable,
                 states: List[str],
                 roles: List[str]) -> None:
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
        file_names: List[str], required
            file names one of which incoming file should have to serve the route
            if empty, every filename is valid
        mime_types: List[str], required
            MIME-types one of which incoming file should have to serve the route
            if empty, every MIME-type is valid
        """
        super().__init__(callback, states, roles)

        self.file_names = file_names
        self.mime_types = mime_types

