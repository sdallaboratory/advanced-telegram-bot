from typing import List, Callable

import telegram as tg
import telegram.ext as tg_ext

from components import *
from .exceptions.initexception import InitException


class TelegramBot:
    """
    Class providing general utils managing and telegram bot creating

    Available utils:
        - Locale-dependent reply/data storage
        - Logging and managing logs
        - Role/authorization system
        - State system
        - User metadata storage

    ..........
    Attributes
    ----------
    role_auth: RoleAuth, public
        role/authorization system
    state_manager: StateManager, public
        state system
    user_meta: UserMetaStorage, public
        user metadata storage
    locale_manager: LocaleManager, public
        locale-dependent reply/data storage
    logger: BotLogger, public
        logger/logs manager
    updater: telegram.ext.Updater, private
        `python-telegram-bot` class, providing a frontend to telegram bot
    dispatcher: telegram.ext.Dispatcher, private
        `python-telegram-bot` class, dispatching all kinds of updates
    routes: dict, private
        list of registered handlers considering roles and states
        should have structure like
        {
            'commands': [
                '<command>': {
                    'function': callback function with **kwargs,
                    'roles': list of user roles allowed to execute callback function,
                    'states': list of user states allowed to execute callback function,
                },
                ...
            ],
            'messages': [
                '<message>': {
                    'function': callback function with **kwargs,
                    'roles': list of user roles allowed to execute callback function,
                    'states': list of user states allowed to execute callback function,
                },
                ...
            ]
        }

    .......
    Methods
    -------
    route(): public
        decorator providing registering command/message handlers considering roles and states
    send_message(): public
        sends message to user
    start(): public
        starts bot and sets it to idle
    stop(): public
        stops bot
    init(): private
        class constructor
    has_access(): private
        checks if user has access to execute callback function
    register_command_service(): private
        registers given command handler
    register_message_service(): private
        registers given message handler
    serve_command(): private
        handler for all registered commands, distributes callback functions to received commands
    serve_message(): private
        handler for all registered messages, distributes callback functions to received messages
    """
    def __init__(self,
                 bot_token: str,
                 roles: dict,
                 states: list,
                 users_collection_name: str = "Users",
                 logs_collection_name: str = "Logs",
                 locales_folder: str = "Locales",
                 state_with_params: bool = False,
                 **storage_data) -> None:
        """
        Class constructor

        .........
        Arguments
        ---------
        bot_token: str, required
            telegram bot token got from Bot Father
        roles: dict, required
            dictionary with all roles that will be available for users and passwords for them
            should be structured like
            {
                '<role>': {
                    'password':  string password
                }
            }
            the default role 'user' may be not mentioned, in this case password will be empty string ('')
        states: list, required
            list with all possible states that will be available for users
            the default state 'free' may be not mentioned
        users_collection_name: str, optional (default = 'Users')
            db collection name for users metadata storage
        logs_collection_name: str, optional (default = 'Logs')
            db collection name for logs
        locales_folder: str, optional (default = 'Locales')
            folder containing locale-dependent replies/data
        state_with_params: bool, optional
            flag providing ability to add dict of params to current state
        **storage_data
            all the params connected with db usage:
                db_address: str, required
                    ip address of db
                db_port: Union[int, str], required
                    port of db
                db_username: str, required
                    username that can be used to access db
                db_password: str, required
                    password to given username
                db_name: str, required
                    name of db to connect

        ..........
        Exceptions
        ----------
        InitException
            exception is raised in case of:
            - constructor could not initialize storage class
            - some of required arguments are not provided
        """
        if set(['db_address', 'db_port', 'db_username', 'db_password', 'db_name']).issubset(list(storage_data.keys())):
            storage = MongoDBStorage(address=storage_data['db_address'],
                                    port=int(storage_data['db_port']),
                                    username=storage_data['db_username'],
                                    password=storage_data['db_password'],
                                    database=storage_data['db_name'])
        elif 'storage_folder' in storage_data.keys():
            storage = LocalJSONStorage(storage_data['storage_folder'])
        else:
            raise InitException('Could not initialize storage class')

        params_list = [roles, states, users_collection_name, logs_collection_name, locales_folder]
        for param in params_list:
             if not param:
                 raise InitException(f'{param} cannot be empty!')

        self.role_auth = RoleAuth(storage=storage,
                                  roles=roles,
                                  users_collection=users_collection_name)
        self.state_manager = StateManager(storage=storage,
                                          users_collection=users_collection_name,
                                          with_params=state_with_params)
        self.user_meta = UserMetaStorage(storage=storage,
                                         users_collection=users_collection_name)
        self.locale_manager = LocaleManager(locales_folder=locales_folder)
        self.logger = BotLogger(storage=storage,
                                collection_name=logs_collection_name)

        self.__updater = tg_ext.Updater(token=bot_token)
        self.__dispatcher = self.__updater.dispatcher
        self.__routes = {"commands": [], "messages": []}

    def __has_access(self, user_id: int, states: List[str], roles: List[str]) -> bool:
        """
        Checks if user has access to execute callback function.
        returns True in case user's state is in states list AND
                             user is loginned as one of roles for given list

        .........
        Arguments
        ---------
        user_id: int, required
            id of user to check for access
        states: List[str], required
            list of states that in combination with correct role give access
        roles: List[str], required
            list of roles that in combination with correct state gives access
        """
        has_access = False
        if states and self.state_manager.get_state(user_id) not in states:
            return has_access
        if roles:
            for role in roles:
                if self.role_auth.is_loggined_as(role, user_id):
                    has_access = True
                    break
        return has_access

    def __register_command_service(self, command: str, func: Callable,
                                   states: List[str], roles: List[str]) -> None:
        """
        Registers given command handler.

        .........
        Arguments
        ---------
        command: str, required
            command to register
        func: Callable, required
            callback for given command
        states: List[str], required
            list of states that in combination with correct role give user access to execute callback function
        roles: List[str], required
            list of roles that in combination with correct state give user access to execute callback function
        """
        self.__routes['commands'].append({command: {'function': func, 'states': states, 'roles': roles}})
        self.__dispatcher.add_handler(tg_ext.CommandHandler(command, callback=self.__serve_command))

    def __register_message_service(self, message: str, func: Callable,
                                   states: List[str], roles: List[str]) -> None:
        """
        Registers given message handler.

        .........
        Arguments
        ---------
        message: str, required
            message to register
        func: Callable, required
            callback for given command
        states: List[str], required
            list of states that in combination with correct role give user access to execute callback function
        roles: List[str], required
            list of roles that in combination with correct state give user access to execute callback function
        """
        self.__routes['messages'].append({message: {'function': func, 'states': states, 'roles': roles}})
        self.__dispatcher.add_handler(tg_ext.MessageHandler(filters=tg_ext.Filters.text([message]),
                                                            callback=self.__serve_message))

    def __serve_command(self, update: tg.Update, context: tg_ext.CallbackContext) -> None:
        """
        Handler for all registered commands, distributes callback functions to received commands.
        command is considered to start with '/' and end with end of string or space.
        Calls callback function with **kwargs:
            user_id: int
                chat id that command is received from
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
        user_id = message.chat.id
        command = message.split()[0].strip('/')
        if command not in self.__routes['commands']:
            return

        func = self.__routes['commands'][command]['function']
        states = self.__routes['commands'][command]['states']
        roles = self.__routes['commands'][command]['roles']

        if self.__has_access(user_id, states, roles):
            func(user_id=user_id, message=message)

    def __serve_message(self, update: tg.Update, context: tg_ext.CallbackContext) -> None:
        """
        Handler for all registered messages, distributes callback functions to received messages.
        Calls callback function with **kwargs:
            user_id: int
                chat id that command is received from
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
        user_id = message.chat.id
        if message not in self.__routes['messages']:
            return

        func = self.__routes['messages'][message]['function']
        states = self.__routes['messages'][message]['states']
        roles = self.__routes['messages'][message]['roles']

        if self.__has_access(user_id, states, roles):
            func(user_id=user_id, message=message)

    def route(self, commands: List[str] = None, messages: List[str] = None,
              states: List[str] = None, roles: List[str] = None) -> Callable:
        """
        Decorator providing registering command/message handlers considering roles and states.
        registered handler is accessible only to users with one of given roles AND one of given states.

        .........
        Arguments
        ---------
        commands: List[str], optional (default = None)
            commands to access given handler. if None, no command is registered with given handler
        messages: List[str], optional (default = None)
            messages to access given handler. if None, no message is registered with given handler
        states: List[str], optional (default = None)
            states that provide user's access to execute callback function. if None, callback function is available to everyone
        roles: List[str], optional (default = None)
            roles that provide user's access to execute callback function. if None, callback function is available to everyone
        """
        if states is None:
            states = []
        if roles is None:
            roles = []
        def decorator(func: Callable) -> Callable:
            if commands:
                for command in commands:
                    self.__register_command_service(command, func, states, roles)
            if messages:
                for message in messages:
                    self.__register_message_service(message, func, states, roles)
            return func

        return decorator

    def send_message(self, user_id: int, message: str,
                     reply_keyboard: List[List[str]] = None,
                     reply_keyboard_resize: bool = True) -> None:
        """
        Sends message to user.

        .........
        Arguments
        ---------
        user_id: int, required
            id of user whom to send message
        message: str, required
            text of sending message
        reply_keyboard: List[List[str]], optional (default = None)
            reply keyboard buttons' texts. if None, no reply keyboard is sended with message
        reply_keyboard_resize: bool, optional (default = True)
            flag that requests clients to resize keyboard
        """
        if reply_keyboard:
            reply_keyboard = tg.ReplyKeyboardMarkup(reply_keyboard, reply_keyboard_resize)

        self.__updater.bot.send_message(chat_id=user_id,
                                        text=message,
                                        reply_markup=reply_keyboard)
        self.logger.log_send_msg(id=user_id, text=message)

    def start(self) -> None:
        """
        Starts the bot.
        """
        self.__updater.start_polling()
        self.logger.log_start()
        self.__updater.idle()

    def stop(self) -> None:
        """
        Stops the bot.
        """
        self.__updater.stop()
        self.logger.log_stop()