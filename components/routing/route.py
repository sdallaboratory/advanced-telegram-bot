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
        states user should have to access serving the route
        empty list means that every state is valid
    roles: List[str], public
        roles user should have to access serving the route
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
            states user should have to access serving the route
        roles: List[str]
            roles user should have to access serving the route
        """
        self.callback = callback
        self.states = states
        self.roles = roles

    def is_accessible_with(self, state: str, roles: List[str]) -> bool:
        """
        Checks if route is accessible to serve with given state and roles.
        returns True in case user's state is in states list AND
                             user is loginned as one of roles for given list

        .........
        Arguments
        ---------
        state: str, required
            state that in combination with correct roles gives access
        roles: List[str], required
            list of roles that in combination with correct state give access
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

