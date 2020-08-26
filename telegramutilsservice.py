from role_managing.roleauth import RoleAuth
from state_managing.statemanager import StateManager
from user_meta.usermetastorage import UserMetaStorage
from storage_managing.mongodbstorage import MongoDBStorage
from storage_managing.localjsonstorage import LocalJSONStorage
from locales.localemanager import LocaleManager
from logs.botlogger import BotLogger


class TelegramUtilsService:
    def __init__(self,
                roles: dict,
                states: list,
                user_collection_name: str="Users",
                logs_collection_name: str="Logs",
                state_with_params: bool=False,
                locales_folder: str="Locales",
                **storage_data) -> None:
        if ['db_address', 'port', 'username', 'password', 'database'] == list(storage_data.keys()):
            storage = MongoDBStorage(address=storage_data['db_address'],
                                    port=int(storage_data['db_port']),
                                    username=storage_data['db_username'],
                                    password=storage_data['db_password'],
                                    database=storage_data['db_name'])
        elif 'storage_folder' in storage_data.keys():
            storage = LocalJSONStorage(storage_data['storage_folder'])
        else:
            raise InitException('Could not initialize storage class')

        self.role_auth = RoleAuth(storage=storage, roles=roles, users_collection=user_collection_name)
        self.state_manager = StateManager(storage=storage, users_collection=user_collection_name, with_params=state_with_params)
        self.user_meta = UserMetaStorage(storage=storage, users_collection=user_collection_name)
        self.locale_manager = LocaleManager(locales_folder)
        self.logger = BotLogger(storage=storage, collection_name=logs_collection_name)

class InitException(Exception):
    '''
    TelegramUtilsService constructor's exception class
    '''
