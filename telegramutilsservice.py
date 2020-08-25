from .role_managing.roleauth import RoleAuth
from .state_managing.statemanager import StateManager
from .user_meta.usermetastorage import UserMetaStorage
from .storage_managing.mongodbstorage import MongoDBStorage
from .locales.localemanager import LocaleManager
from .logs.botlogger import BotLogger


class TelegramUtilsService:
    def __init__(self,
                 db_address: str,
                 db_port: str,
                 db_username: str,
                 db_password: str,
                 db_name: str,
                 user_collection_name: str,
                 logs_collection_name: str,
                 roles: dict,
                 states: list,
                 state_with_params: bool,
                 locales_folder: str) -> None:
        storage = MongoDBStorage(address=db_address,
                                 port=int(db_port),
                                 username=db_username,
                                 password=db_password,
                                 database=db_name)
        self.role_auth = RoleAuth(storage=storage, roles=roles, users_collection=user_collection_name)
        self.state_manager = StateManager(storage=storage, users_collection=user_collection_name, with_params=state_with_params)
        self.user_meta = UserMetaStorage(storage=storage, users_collection=user_collection_name)
        self.locale_manager = LocaleManager(locales_folder)
        self.logger = BotLogger(storage=storage, collection_name=logs_collection_name)

