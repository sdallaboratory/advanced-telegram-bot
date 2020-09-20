from ..storage_managing.storage import Storage
from .exceptions.usermetaerror import UserMetaError


class UserMetaStorage:
    '''
    Class for users' meta data handling
    '''
    def __init__(self, storage: Storage, users_collection: str = "Users",
                id_column: str = "_id", username_column: str = "Username",
                first_name_column: str = "First_Name", last_name_column: str = "Last_Name",
                locale_column: str = "Locale"):
        '''
        Parameters
        ----------
        storage : Storage
            pointer to the inherited class from Storage (i.e MongoDBStorage)
        users_collection : str, optional
            name of id column from users_collection, by default "Users"
        id_column : str, optional
            name of id column from users_collection, by default "_id"
        locale_column : str, optional
            name of user's locale column from users_collection, by default "Locale"
        '''
        self.__users_collection = users_collection
        self.__id_column = id_column
        self.__username_column = username_column
        self.__first_name_column = first_name_column
        self.__last_name_column = last_name_column
        self.__locale_column = locale_column

        self.__storage = storage

    def get_locale(self, user_id: int) -> str:
        '''
        Gives a locale of the requested user

        Parameters
        ----------
        user_id : int
            User's id from the storage

        Returns
        -------
        str
            locale code name

        Raises
        ------
        UserMetaError
            Raises an exception if something went wrong
        '''
        locales = self.__storage.get_data_by_column(collection=self.__users_collection,
                                                    by=self.__id_column,
                                                    value=user_id)
        if not locales:
            raise UserMetaError("Meta Exception")

        locale = locales[0]

        return locale[self.__locale_column]

    def user_exists(self, user_id: int) -> bool:
        '''
        Checks whether user exists or not

        Parameters
        ----------
        user_id : int
            User's id from the storage

        Returns
        -------
        bool
            "True" if user exists else "False"
        '''
        users = self.__storage.get_data_by_column(self.__users_collection, self.__id_column, user_id)

        return True if users else False

    def user_initialize(self, user_id: int, init_dict: dict):
        '''
        User initialization method. Should be  used to add new user to the storage.

        Parameters
        ----------
        user_id : int
            User's id
        init_dict : dict
            Initialization dictionary
            ... example:
            {
                "Locale": "en_us",
                "Roles": ["user"],
                "State": "free",
                "State_Params": {}
            }
        '''
        if not self.user_exists(user_id):
            init_dict[self.__id_column] = user_id

            self.__storage.insert_one_doc(self.__users_collection, init_dict)

    def user_update(self, user_id: int, username: str = "", first_name: str = "", last_name: str = ""):
        '''
        Method for updating user's data in the storage.

        Parameters
        ----------
        user_id : int
            User's id from the storage
        username : str, optional
            User's username, by default ""
        first_name : str, optional
            User's first name, by default ""
        last_name : str, optional
            User's last name, by default ""

        Raises
        ------
        UserMetaError
            [description]
        '''
        upd_dict = {
            self.__username_column: username,
            self.__first_name_column: first_name,
            self.__last_name_column: last_name
        }
        try:
            self.__storage.update_one_doc(self.__users_collection, self.__id_column, user_id, upd_dict)
        except:
            raise UserMetaError("Failed to update user")

    def get_username(self, user_id: int) -> str:
        '''
        Gives user's username

        Parameters
        ----------
        user_id : int
            User's id from the storage
        Returns
        -------
        str
            username
        '''
        try:
            user_id = int(user_id)

            usernames_found = self.__storage.get_data_by_column(self.__users_collection,
                                                            by=self.__id_column,
                                                            value=user_id,
                                                            columns=[self.__username_column])

            username = usernames_found[0]
            username = username[self.__username_column]
            return username
        except:
            raise UserMetaError("User was not found!")

    def get_first_name(self, user_id: int) -> str:
        '''
        Gives user's first name

        Parameters
        ----------
        user_id : int
            User's id from the storage
        Returns
        -------
        str
            first name
        '''
        try:
            user_id = int(user_id)

            first_name_found = self.__storage.get_data_by_column(self.__users_collection,
                                                                by=self.__id_column,
                                                                value=user_id,
                                                                columns=[self.__first_name_column])

            first_name = first_name_found[0]
            first_name = first_name[self.__first_name_column]
            return first_name
        except:
            raise UserMetaError("User was not found!")

    def get_last_name(self, user_id: int) -> str:
        '''
        Gives user's last name

        Parameters
        ----------
        user_id : int
            User's id from the storage
        Returns
        -------
        str
            last name
        '''
        try:
            user_id = int(user_id)

            last_name_found = self.__storage.get_data_by_column(self.__users_collection,
                                                                by=self.__id_column,
                                                                value=user_id,
                                                                columns=[self.__last_name_column])

            last_name = last_name_found[0]
            last_name = last_name[self.__last_name_column]
            return last_name
        except:
            raise UserMetaError("User was not found!")

