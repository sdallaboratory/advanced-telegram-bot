import telegram as tg
import telegram.ext as tg_ext

from components import *
from .exceptions.initexception import InitException

class TelegramBot:
    def __init__(self,
                 bot_token: str,
                 roles: dict,
                 states: list,
                 users_collection_name: str="Users",
                 logs_collection_name: str="Logs",
                 locales_folder: str="Locales",
                 state_with_params: bool=False,
                 **storage_data) -> None:
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
