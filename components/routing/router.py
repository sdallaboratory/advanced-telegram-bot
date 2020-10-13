import re
from typing import List

import telegram as tg
import telegram.ext as tg_ext

from ..state_managing.statemanager import StateManager
from ..state_managing.exceptions.stateerror import StateError
from ..role_managing.roleauth import RoleAuth
from ..role_managing.exceptions.roleerror import RoleError

from .commandroute import CommandRoute
from .messageroute import MessageRoute


class Router:
    """
    Class managing income messages callbacks

    ..........
    Attributes
    ----------
    message_routes: List[MessageRoute], private
        list of text message routes
    command_routes: List[CommandRoute], private
        list of commands routes (commands start with /)
    tg: telegram.ext.Dispatcher, private
        `python-telegram-bot` class, dispatching all kinds of updates
    state_manager: StateManager, private
        class managing user states
    role_auth: RoleAuth, private
        class managing user roles

    .......
    Methods
    -------
    register_command_route(): public
        registers given command handler
    register_message_route(): public
        registers given message handler
    find_command_routes(): private
        finds all command routes that are accessible with user state and roles and triggered with command
    find_message_routes(): private
        finds all message routes that are accessible with user state and roles and triggered with message
    serve_command_route(): private
        handler for all registered commands, distributes callback functions to received commands
    serve_message_route(): private
        handler for all registered messages, distributes callback functions to received messages
    """
    def __init__(self,
                 tg_dispatcher: tg_ext.Dispatcher,
                 state_manager: StateManager,
                 role_auth: RoleAuth) -> None:
        """
        Constructor.

        .........
        Arguments
        ---------
        tg_dispatcher: telegram.ext.Dispatcher, required
            `python-telegram-bot` class, dispatching all kinds of updates
        state_manager: StateManager, required
            state system
        role_auth: RoleAuth, required
            role/authorization system
        """
        self.__message_routes: List[MessageRoute] = []
        self.__command_routes: List[CommandRoute] = []

        self.__tg = tg_dispatcher
        self.__state_manager = state_manager
        self.__role_auth = role_auth

    def __find_command_routes(self,
                              command: str,
                              state: str,
                              roles: List[str]) -> List[CommandRoute]:
        """
        Finds all command routes that are accessible with user state and roles and triggered with command

        .........
        Arguments
        ---------
        command: str, requited
            trigger command to serve the route
        state: str, required
            user state for access to serving the route
        roles: List[str], required
            user roles for access to serving the route
        """
        found_routes = []

        for command_route in self.__command_routes:
            if command == command_route.command and\
               command_route.is_accessible_with(state, roles):
                found_routes.append(command_route)
        return found_routes

    def __find_message_routes(self,
                              message: str,
                              state: str,
                              roles: List[str]) -> List[MessageRoute]:
        """
        Finds all message routes that are accessible with user state and roles and triggered with message

        .........
        Arguments
        ---------
        message: str, requited
            trigger regex message text to serve the route
        state: str, required
            user state for access to serving the route
        roles: List[str], required
            user roles for access to serving the route
        """
        found_routes = []

        for message_route in self.__message_routes:
            if re.fullmatch(message_route.message, message) and\
               message_route.is_accessible_with(state, roles):
                found_routes.append(message_route)
        return found_routes

    def __serve_command_route(self, update: tg.Update, context: tg_ext.CallbackContext) -> None:
        """
        Handler for all registered commands, distributes callback functions to received commands.
        command is considered to start with '/' and end with end of string or space.
        Calls callback function with **kwargs:
            user_id: int
                chat id that command is received from
            message: str
                full received message text
            username: str
                telegram username of user with user_id
            first_name: str
                telegram first name of user with user_id
            last_name: str
                telegram last name of user with user_id
            roles: List[str]
                roles of user with user_id
            state: Union[str, dict]
                state of user presented by state_name if 'state_with_params' was True,
                otherwise it is presented as dict with keys 'State' and 'State_Params' by default

        .........
        Arguments
        ---------
        update: telegram.Update, required
            `python-telegram-bot` class, representing an incoming update
        context: telegram.ext.CallbackContext, required
            `python-telegram-bot` class. context passed by telegram handler to callback
        """
        message = update.message
        chat = message.chat

        message = message.text
        user_id = chat.id
        username = chat.username
        first_name = chat.first_name
        last_name = chat.last_name

        command = message.split()[0].strip('/')
        try: # try-except for user start initialization when he is not in db
            user_state = self.__state_manager.get_state(user_id)
            user_roles = self.__role_auth.get_user_roles(user_id)
        except (StateError, RoleError):
            user_state = 'free'
            user_roles = ['user']

        found_routes = self.__find_command_routes(command, user_state, user_roles)

        for route in found_routes:
            route.callback(user_id=user_id,
                           message=message,
                           username=username,
                           first_name=first_name,
                           last_name=last_name,
                           roles=user_roles,
                           state=user_state)

    def __serve_message_route(self, update: tg.Update, context: tg_ext.CallbackContext) -> None:
        """
        Handler for all registered messages, distributes callback functions to received messages.
        Calls callback function with **kwargs:
            user_id: int
                chat id that command is received from
            message: str
                full received message text
            username: str
                telegram username of user with user_id
            first_name: str
                telegram first name of user with user_id
            last_name: str
                telegram last name of user with user_id
            roles: List[str]
                roles of user with user_id
            state: Union[str, dict]
                state of user presented by state_name if 'state_with_params' was True,
                otherwise it is presented as dict with keys 'State' and 'State_Params' by default

        .........
        Arguments
        ---------
        update: telegram.Update, required
            `python-telegram-bot` class, representing an incoming update
        context: telegram.ext.CallbackContext, required
            `python-telegram-bot` class. context passed by telegram handler to callback
        """
        message = update.message
        chat = message.chat

        message = message.text
        user_id = chat.id
        username = chat.username
        first_name = chat.first_name
        last_name = chat.last_name

        try: # try-except for user start initialization when he is not in db
            user_state = self.__state_manager.get_state(user_id)
            user_roles = self.__role_auth.get_user_roles(user_id)
        except (StateError, RoleError):
            user_state = 'free'
            user_roles = ['user']

        found_routes = self.__find_message_routes(message, user_state, user_roles)

        for route in found_routes:
            route.callback(user_id=user_id,
                           message=message,
                           username=username,
                           first_name=first_name,
                           last_name=last_name,
                           roles=user_roles,
                           state=user_state)

    def register_command_route(self, route: CommandRoute) -> None:
        """
        Registers given command handler.

        .........
        Arguments
        ---------
        route: CommandRoute, required
            route to register
        """
        self.__command_routes.append(route)
        self.__tg.add_handler(tg_ext.CommandHandler(command=route.command,
                                                    callback=self.__serve_command_route))

    def register_message_route(self, route: MessageRoute) -> None:
        """
        Registers given text message handler.

        .........
        Arguments
        ---------
        route: MessageRoute, required
            route to register
        """
        self.__message_routes.append(route)
        self.__tg.add_handler(tg_ext.MessageHandler(filters=tg_ext.Filters.regex(route.message),
                                                    callback=self.__serve_message_route))

