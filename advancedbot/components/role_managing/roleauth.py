from ..utils.filemanager import FileManager

from ..storage_managing.storage import Storage

from .exceptions.passworderror import PasswordError
from .exceptions.roleerror import RoleError
from .exceptions.alreadyloggederror import AlreadyLoggedError


class RoleAuth:
    '''
    A class made for simplifiying users' roles management
    '''
    def __init__(self, storage: Storage, roles: dict, users_collection: str = "Users",
                id_column: str = "_id", roles_column: str = "Roles"):
        '''
        Parameters
        ----------
        storage : Storage
            pointer to the inherited class from Storage (i.e MongoDBStorage)
        roles : dict
            a dictionary of roles
            ...
            example:
                {
                    "admin": {
                        "password": "admin-pass"
                    },
                    "user": {
                        "password": ""
                    }
                }
            ...
        users_collection : str, optional
            name of id column from users_collection, by default "Users"
        id_column : str, optional
            name of id column from users_collection, by default "_id"
        roles_column : str, optional
            name of roles column from users_collection, by default "Roles"
        '''
        self.__users_collection = users_collection
        self.__id_column = id_column
        self.__roles_column = roles_column

        self.__storage = storage
        self.__roles = roles

    def __role_check(self, role: str) -> None:
        '''
        Checks if role exists
        Parameters
        ----------
        role : str
            role name to check

        Raises
        ------
        RoleError
            Exception raises when role does not exist
        '''
        if not role in self.__roles:
            raise RoleError("Role is not found!")

    def __password_check(self, role: str, password: str) -> None:
        if self.__roles[role]['password'] != password:
            raise PasswordError("Wrong password!")

    def get_list_of_roles(self) -> list:
        '''
        Gives list of all available roles

        Returns
        -------
        list
            list of roles
        '''
        return list(self.__roles.keys())

    def add_role(self, role: str, password: str = "") -> None:
        '''
        Adds role to the list of roles

        Parameters
        ----------
        role : str
            Role's name
        password : str, optional
            Password for the role, by default ""
        '''
        self.__roles[role] = {}
        self.__roles[role]['password'] = password

    def remove_role(self, role: str, password: str = "") -> None:
        '''
        Removes specified role from the roles list

        Parameters
        ----------
        role : str
            Role's name
        password : str, optional
            Password for the role, by default ""
        '''
        self.__role_check(role)
        self.__password_check(role, password)

        self.__roles.pop(role)

#    def rename_role(self, role: str) -> None:
#        pass

    def get_user_roles(self, user_id: int) -> list:
        '''
        Gives a list of requested user's roles

        Parameters
        ----------
        user_id : int
            user's id from the storage

        Returns
        -------
        list
            list of user's roles

        Raises
        ------
        RoleError
            Raises an exception when user was not found
        '''
        roles = self.__storage.get_data_by_column(collection=self.__users_collection,
                                                    by=self.__id_column,
                                                    value=user_id)
        if not roles:
            raise RoleError("User not found!")

        role = roles[0]

        return role[self.__roles_column]

    def is_loggined_as(self, role: str, user_id: int) -> bool:
        '''
        Checks if user is logged in as requested role

        Parameters
        ----------
        role : str
            Role's name
        user_id : int
            user's id from the storage

        Returns
        -------
        bool
            whether user is logged in or not
        '''
        user_roles = self.get_user_roles(user_id)

        return True if role in user_roles else False

    def login_as(self, role: str, user_id: int, password: str="") -> None:
        '''
        Logs in specified user as a specified role with

        Parameters
        ----------
        role : str
            Role's name
        user_id : int
            User's id from the storage
        password : str
            Roles's password

        Raises
        ------
        AlreadyLoggedError
            Raises an exception if user is already logged in
        '''
        self.__role_check(role)
        self.__password_check(role, password)

        user_roles = self.get_user_roles(user_id)

        if role not in user_roles:
            user_roles.append(role)

            roles_dict = {
                self.__roles_column: user_roles
            }

            self.__storage.update_one_doc(collection=self.__users_collection,
                                        id_column=self.__id_column,
                                        id=user_id,
                                        doc=roles_dict)

        else:
            raise AlreadyLoggedError(f'User has already logged in as a(n) {role}!')

    def logout_as(self, role: str, user_id: int) -> None:
        '''
        Logs the user out

        Parameters
        ----------
        role : str
            Role's name
        user_id : int
            User's id from the storage

        Raises
        ------
        AlreadyLoggedError
            Raises an exception if user was not logged in
        '''
        self.__role_check(role)

        user_roles = self.get_user_roles(user_id)
        if role in user_roles:
            user_roles.remove(role)

            roles_dict = {
                self.__roles_column: user_roles
            }

            self.__storage.update_one_doc(collection=self.__users_collection,
                                        id_column=self.__id_column,
                                        id=user_id,
                                        doc=roles_dict)

        else:
            raise AlreadyLoggedError(f'User has already logged out as a(n) {role}!')
