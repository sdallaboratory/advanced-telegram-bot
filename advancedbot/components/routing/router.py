import re
from typing import List

import telegram as tg
import telegram.ext as tg_ext

from ..models import DocumentLink, User
from ..state_managing.statemanager import StateManager
from ..state_managing.exceptions.stateerror import StateError
from ..role_managing.roleauth import RoleAuth
from ..role_managing.exceptions.roleerror import RoleError

from .routes import CommandRoute, DocumentRoute, ImageRoute, MessageRoute


class Router:
    """
    Class managing income messages callbacks

    ..........
    Attributes
    ----------
    command_routes: List[CommandRoute], private
        list of commands routes (commands start with /)
    document_routes: List[DocumentRoute], private
        list of document routes
    image_routes: List[MessageRoute], private
        list of image (photo) routes
    message_routes: List[MessageRoute], private
        list of text message routes
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
    register_document_route(): public
        registers given document handler
    register_image_route(): public
        registers given image handler
    register_message_route(): public
        registers given message handler
    find_command_routes(): private
        finds all command routes that are accessible with user state and roles and triggered with command
    find_document_routes(): private
        finds all documents routes that are accessible with user state and roles and triggered with document
    find_image_routes(): private
        finds all image routes that are accessible with user state and roles and triggered with image
    find_message_routes(): private
        finds all message routes that are accessible with user state and roles and triggered with message
    serve_command_route(): private
        handler for all registered commands, distributes callback functions to received commands
    serve_document_route(): private
        handler for all registered documents, distributes callback functions to received documents
    serve_image_route(): private
        handler for all registered images, distributes callback functions to received images
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
        self.__doсument_routes: List[DocumentRoute] = []
        self.__image_routes: List[ImageRoute] = []

        self.__tg = tg_dispatcher
        self.__state_manager = state_manager
        self.__role_auth = role_auth

    def __find_command_routes(self,
                              command: str,
                              state: str,
                              roles: List[str]) -> List[CommandRoute]:
        """
        Finds all command routes that are accessible with user state and roles
        and triggered with command

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

    def __find_document_routes(self,
                               file_name: str,
                               mime_type: str,
                               state: str,
                               roles: List[str]) -> List[DocumentRoute]:
        """
        Finds all document routes that are accessible with user state and roles
        and triggered by a document with given name and MIME-type

        .........
        Arguments
        ---------
        file_name: str, requited
            trigger document file name to serve the route
        mime_type: str, requited
            trigger document MIME-type to serve the route
        state: str, required
            user state for access to serving the route
        roles: List[str], required
            user roles for access to serving the route
        """
        found_routes = []

        for route in self.__doсument_routes:
            if route.file_names and not file_name in route.file_names:
                continue
            if route.mime_types and not mime_type in route.mime_types:
                continue
            if not route.is_accessible_with(state, roles):
                continue
            found_routes.append(route)

        return found_routes

    def __find_image_routes(self,
                            state: str,
                            roles: List[str]) -> List[ImageRoute]:
        """
        Finds all image routes that are accessible with user state and roles
        and triggered by an image

        .........
        Arguments
        ---------
        state: str, required
            user state for access to serving the route
        roles: List[str], required
            user roles for access to serving the route
        """
        found_routes = []

        for route in self.__image_routes:
            if not route.is_accessible_with(state, roles):
                continue
            found_routes.append(route)

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
            user: User
                user who has sent a command
            message: str
                full received message text

        .........
        Arguments
        ---------
        update: telegram.Update, required
            `python-telegram-bot` class, representing an incoming update
        context: telegram.ext.CallbackContext, required
            `python-telegram-bot` class. context passed by telegram handler to callback
        """
        message = update.message

        text = message.text
        command = text.split()[0].strip('/')

        user = User(message.chat)
        try: # try-except for user start initialization when he is not in db
            user.state = self.__state_manager.get_state(user.id)
            user.roles = self.__role_auth.get_user_roles(user.id)
        except (StateError, RoleError):
            user.state = 'free'
            user.roles = ['user']

        found_routes = self.__find_command_routes(command, user.state, user.roles)
        for route in found_routes:
            route.callback(user=user,
                           message=text)

    def __serve_document_route(self, update: tg.Update, context: tg_ext.CallbackContext) -> None:
        """
        Handler for all registered documents, distributes callback functions to received documents.
        Calls callback function with **kwargs:
            user: User
                user who has sent a document
            message: str
                full received message text
            document: DocumentLink
                link to received document

        .........
        Arguments
        ---------
        update: telegram.Update, required
            `python-telegram-bot` class, representing an incoming update
        context: telegram.ext.CallbackContext, required
            `python-telegram-bot` class. context passed by telegram handler to callback
        """
        message: tg.Message = update.message

        text = message.text

        user = User(message.chat)
        try: # try-except for user start initialization when he is not in db
            user.state = self.__state_manager.get_state(user.id)
            user.roles = self.__role_auth.get_user_roles(user.id)
        except (StateError, RoleError):
            user.state = 'free'
            user.roles = ['user']

        document_link = DocumentLink(tg_document=message.document,
                                     media_group_id=message.media_group_id)

        found_routes = self.__find_document_routes(document_link.name,
                                                   document_link.mime_type,
                                                   user.state, user.roles)
        for route in found_routes:
            route.callback(user=user,
                           message=text,
                           document=document_link)

    def __serve_image_route(self, update: tg.Update, context: tg_ext.CallbackContext) -> None:
        """
        Handler for all registered images, distributes callback functions to received images.
        Calls callback function with **kwargs:
            user: User
                user who has sent an image
            message: str
                full received message text
            images: List[DocumentLink]
                links to received images

        .........
        Arguments
        ---------
        update: telegram.Update, required
            `python-telegram-bot` class, representing an incoming update
        context: telegram.ext.CallbackContext, required
            `python-telegram-bot` class. context passed by telegram handler to callback
        """
        message: tg.Message = update.message

        text = message.text

        user = User(message.chat)
        try: # try-except for user start initialization when he is not in db
            user.state = self.__state_manager.get_state(user.id)
            user.roles = self.__role_auth.get_user_roles(user.id)
        except (StateError, RoleError):
            user.state = 'free'
            user.roles = ['user']

        image_ids = message.photo
        images = [DocumentLink(image_id.get_file(), message.media_group_id) \
                  for image_id in image_ids]

        found_routes = self.__find_image_routes(user.state, user.roles)
        for route in found_routes:
            route.callback(user=user,
                           message=text,
                           images=images)

    def __serve_message_route(self, update: tg.Update, context: tg_ext.CallbackContext) -> None:
        """
        Handler for all registered text messages, distributes callback functions to received messages.
        Calls callback function with **kwargs:
            user: User
                user who has sent a message
            message: str
                full received message text

        .........
        Arguments
        ---------
        update: telegram.Update, required
            `python-telegram-bot` class, representing an incoming update
        context: telegram.ext.CallbackContext, required
            `python-telegram-bot` class. context passed by telegram handler to callback
        """
        message = update.message

        text = message.text

        user = User(message.chat)
        try: # try-except for user start initialization when he is not in db
            user.state = self.__state_manager.get_state(user.id)
            user.roles = self.__role_auth.get_user_roles(user.id)
        except (StateError, RoleError):
            user.state = 'free'
            user.roles = ['user']

        found_routes = self.__find_message_routes(text, user.state, user.roles)
        for route in found_routes:
            route.callback(user=user,
                           message=text)

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

    def register_document_route(self, route: DocumentRoute) -> None:
        """
        Registers given document handler.

        .........
        Arguments
        ---------
        route: DocumentRoute, required
            route to register
        """
        self.__doсument_routes.append(route)
        self.__tg.add_handler(tg_ext.MessageHandler(filters=tg_ext.Filters.document,
                                                    callback=self.__serve_document_route))

    def register_image_route(self, route: ImageRoute) -> None:
        """
        Registers given image handler.

        .........
        Arguments
        ---------
        route: ImageRoute, required
            route to register
        """
        self.__image_routes.append(route)
        self.__tg.add_handler(tg_ext.MessageHandler(filters=tg_ext.Filters.photo,
                                                    callback=self.__serve_image_route))

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

