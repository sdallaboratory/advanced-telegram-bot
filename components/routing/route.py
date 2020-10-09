from typing import Callable, List


class Route:
    """
    Class managing single income message.

    ..........
    Attributes
    ----------
    callback: Callable, public
        function to be called when route is served
    states: List[str], public
        states one of which user should have to access serving the route
        empty list means that every state is valid
    roles: List[str], public
        roles one of which user should have to access serving the route
        empty list means that every role is valid
    """
    def __init__(self,
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
        states: List[str]
            states one of which user should have to access serving the route
        roles: List[str]
            roles one of which user should have to access serving the route
        """
        self.callback = callback
        self.states = states
        self.roles = roles

    def is_accessible_with(self, state: str, roles: List[str]) -> bool:
        """
        Checks if route is accessible to serve with given state and roles.
        returns True in case user's state is in states list AND
                             user is loginned as one of roles in given list

        .........
        Arguments
        ---------
        state: str, required
            user state to check for access to serving the route
        roles: List[str], required
            user roles to check for access to serving the route
        """
        if self.states and state not in self.states:
            return False

        if self.roles:
            for role in self.roles:
                if role in roles:
                    return True
        else:
            return True

        return False

