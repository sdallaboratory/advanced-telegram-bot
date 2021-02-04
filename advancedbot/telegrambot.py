import re
from typing import List, Callable

import telegram as tg
import telegram.ext as tg_ext

from .components import *
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
    storage: Storage, public
        common storage for all systems (utils)
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
    sender: MessageSender, public
        outcoming messages manager
    router: Router, private
        incoming messages callback manager
    .......
    Methods
    -------
    document_route(): public
        decorator providing registering document handlers considering roles and states
    image_route(): public
        decorator providing registering image handlers considering roles and states
    route(): public
        decorator providing registering command/message handlers considering roles and states
    start(): public
        starts bot and sets it to idle
    stop(): public
        stops bot
    init(): private
        class constructor
    init_storage(): private
        builds storage
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
            to set role without password, set 'password' value to ''
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
        self.storage = self.__init_storage(storage_data)

        params_list = [roles, states]
        for param in params_list:
             if not param:
                 raise InitException(f'{param} cannot be empty!')

        self.role_auth = RoleAuth(storage=self.storage,
                                  roles=roles,
                                  users_collection=users_collection_name)
        self.__state_params = state_with_params
        self.state_manager = StateManager(storage=self.storage,
                                          users_collection=users_collection_name,
                                          with_params=self.__state_params)
        self.user_meta = UserMetaStorage(storage=self.storage,
                                         users_collection=users_collection_name)
        self.locale_manager = LocaleManager(locales_folder=locales_folder)
        self.logger = BotLogger(storage=self.storage,
                                collection_name=logs_collection_name)

        self.__updater = tg_ext.Updater(token=bot_token,
                                        use_context=True)
        self.__dispatcher = self.__updater.dispatcher

        self.sender = MessageSender(self.__updater, self.logger)
        self.__router = Router(self.__dispatcher, self.state_manager, self.role_auth)

        self.__router.register_command_route(CommandRoute('start', self.__init_user, [], []))

    def __init_storage(self, kwargs: dict) -> Storage:
        """
        Returns initialized Storage class with given args.

        .........
        Arguments
        ---------
        kwargs: dict, required
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
        """
        if set(['db_address', 'db_port', 'db_username', 'db_password', 'db_name']).issubset(list(kwargs.keys())):
            return MongoDBStorage(address=kwargs['db_address'],
                                  port=int(kwargs['db_port']),
                                  username=kwargs['db_username'],
                                  password=kwargs['db_password'],
                                  database=kwargs['db_name'])
        elif 'storage_folder' in kwargs.keys():
            return LocalJSONStorage(kwargs['storage_folder'])
        else:
            raise InitException('Could not initialize storage class')

    def __init_user(self, **kwargs) -> None:
        user: User = kwargs['user']
        self.user_meta.user_initialize(user.id, init_dict={
                'Roles': ['user'],
                'State': 'free',
                'State_Params': []
            })
        self.user_meta.user_update(user_id=user.id,
                                   username=user.username,
                                   first_name=user.first_name,
                                   last_name=user.last_name)

    def document_route(self,
                       file_names: List[str] = None,
                       mime_types: List[str] = None,
                       states: List[str] = None,
                       roles: List[str] = None) -> Callable:
        """
        Decorator providing registering document message handlers considering roles and states.
        registered handler is accessible only to users with one of given roles AND one of given states.

        .........
        Arguments
        ---------
        file_names: List[str], optional (default = None)
            file names to access given handler. If None, every document that satisfies other criteria is able to trigger the handler.
        mime_types: List[str], optional (default = None)
            MIME-types to access given handler. If None, every document that satisfies other criteria is able to trigger the handler.
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
            self.__router.register_document_route(
                    DocumentRoute(file_names, mime_types, func, states, roles))
            return func

        return decorator

    def image_route(self,
                    states: List[str] = None,
                    roles: List[str] = None) -> Callable:
        """
        Decorator providing registering image message handlers considering roles and states.
        registered handler is accessible only to users with one of given roles AND one of given states.

        .........
        Arguments
        ---------
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
            self.__router.register_image_route(
                    ImageRoute(func, states, roles))
            return func

        return decorator

    def route(self,
              commands: List[str] = None,
              messages: List[str] = None,
              states: List[str] = None,
              roles: List[str] = None) -> Callable:
        """
        Decorator providing registering command/text message handlers considering roles and states.
        registered handler is accessible only to users with one of given roles AND one of given states.

        .........
        Arguments
        ---------
        commands: List[str], optional (default = None)
            commands to access given handler. If None, no command is registered with given handler
        messages: List[str], optional (default = None)
            messages to access given handler. If None, no message is registered with given handler. Uses regex.
        states: List[str], optional (default = None)
            states that provide user's access to execute callback function. if None, callback function is available to everyone
        roles: List[str], optional (default = None)
            roles that provide user's access to execute callback function. if None, callback function is available to everyone
        """
        if states is None:
            states = []
        if roles is None:
            roles = []
        if not commands and not messages:
            messages = ['(?s).*'] # matches every message
        def decorator(func: Callable) -> Callable:
            if commands:
                for command in commands:
                    self.__router.register_command_route(
                            CommandRoute(command, func, states, roles))
            if messages:
                for message in messages:
                    self.__router.register_message_route(
                            MessageRoute(message, func, states, roles))
            return func

        return decorator

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
