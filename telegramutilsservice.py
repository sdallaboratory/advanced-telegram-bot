from role_managing.roleauth import RoleAuth
from state_managing.statemanager import StateManager
from user_meta.usermetastorage import UserMetaStorage
from storage_managing.mongodbstorage import MongoDBStorage
from storage_managing.localjsonstorage import LocalJSONStorage
from locales.localemanager import LocaleManager
from logs.botlogger import BotLogger


class InitException(Exception):
    '''
    TelegramUtilsService constructor's exception class
    '''

class TelegramUtilsService:
    '''
    Class that provides methods for:
        ● Locale-dependent data storing
        ● Logging
        ● Role system
        ● State system
        ● User meta data storing

    ...
    Attributes
    ----------
    roles : dict
        A dict or roles. Keys of the dict are roles' titles. For example:
        {
            "admin": {
                "password": "qwerty",
                ... any info you want to provide to role goes here...
            },
            "user": "" (may be empty but it's not recommended)
        }
    states : list
        The list of status' titles. For example:
        ["free", "busy", "entering password"]
    users_collection_name : str, optional
        Name of collection with users. That's a name of json file with data,
        in case you choose json data storage,
        else it's mongo's collection name, by default "Users"
    logs_collection_name : str, optional
        Name of collection where you want logs to be dumped, by default "Logs"
    state_with_params : bool, optional
        Whether you want to use additional parameters for the statments, by default False
        For example:
        {
            "_id": 0,
            "Username": minish144,
            "State": "feedback writing",
            "State_Params": {
                "Feedback_Type": "type1"
            }
        }
    locales_folder : str, optional
        Folder where you store your locales, by default "Locales"
    '''
    def __init__(self,
                roles: dict,
                states: list,
                users_collection_name: str="Users",
                logs_collection_name: str="Logs",
                state_with_params: bool=False,
                locales_folder: str="Locales",
                **storage_data) -> None:
        '''
        Parameters
        ----------
        roles : dict
            A dict or roles. Keys of the dict are roles' titles. For example:
            {
                "admin": {
                    "password": "qwerty",
                    ... any info you want to provide to role goes here...
                },
                "user": "" (may be empty but it's not recommended)
            }
        states : list
            The list of status' titles. For example:
            ["free", "busy", "entering password"]
        users_collection_name : str, optional
            Name of collection with users. That's a name of json file with data,
            in case you choose json data storage,
            else it's mongo's collection name, by default "Users"
        logs_collection_name : str, optional
            Name of collection where you want logs to be dumped, by default "Logs"
        state_with_params : bool, optional
            Whether you want to use additional parameters for the statments, by default False
            For example:
            {
                "_id": 0,
                "Username": minish144,
                "State": "feedback writing",
                "State_Params": {
                    "Feedback_Type": "type1"
                }
            }
        locales_folder : str, optional
            Folder where you store your locales, by default "Locales"

        Raises
        ------
        InitException
            Exception raises in case constructor could not initialize storage class
        InitException
            Exception raises in case some of necessary parameters is empty
        '''
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

        params_list = [roles, states, users_collection_name, logs_collection_name]
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
