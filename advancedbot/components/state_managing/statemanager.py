from typing import Union

from ..storage_managing.storage import Storage
from .exceptions.stateerror import StateError


class StateManager:
    '''
    Class for managing users' state
    '''
    def __init__(self, storage: Storage, users_collection: str = "Users",
                    id_column: str = "_id", status_column: str = "State",
                    params_column: str = "State_Params", free_status: str = "free",
                    with_params: bool = False):
        '''
        Parameters
        ----------
        storage : Storage
            pointer to the inherited class from Storage (i.e MongoDBStorage)
        users_collection : str, optional
            name of id column from users_collection, by default "Users"
        id_column : str, optional
            name of id column from users_collection, by default "_id"
        status_column : str, optional
            name of status column from users_collection, by default "State"
        params_column : str, optional
            name of state parameters column from users_collection, by default "State_Params"
        free_status : str, optional
            value of "free" status, by default "free"
        with_params : bool, optional
            whether to use params or not, by default False
        '''
        self.__users_collection = users_collection
        self.__id_column = id_column
        self.__status_column = status_column
        self.__params_column = params_column

        self.__free_status = free_status

        self.__storage = storage
        self.__with_params = with_params

    def get_state(self, user_id: int) -> str:
        '''
        Gives a state of specified user

        Parameters
        ----------
        user_id : int
            User's id from the storage

        Returns
        -------
        str
            user's status string

        Raises
        ------
        StateError
            Raises an exception if user was not found
        '''
        # if self.__with_params:
        #     columns = [self.__status_column, self.__params_column]
        # else:
        columns = [self.__status_column]

        response = self.__storage.get_data_by_column(collection=self.__users_collection,
                                                    by=self.__id_column,
                                                    value=user_id,
                                                    columns=columns)
        if not response:
            raise StateError("User was not found!")

        state = response[0]

        # if self.__with_params:
        #     return state
        # else:
        return state[self.__status_column]

    def get_state_params(self, user_id: int) -> dict:
        '''
        Gives a state params of specified user

        Parameters
        ----------
        user_id : int
            User's id from the storage

        Returns
        -------
        dict
            user's state_params if with_params = True

        Raises
        ------
        StateError
            Raises an exception if user was not found
        '''
        if not self.__with_params:
            raise StateError("Class was initialized with no params")
        columns = [self.__params_column]

        response = self.__storage.get_data_by_column(collection=self.__users_collection,
                                                    by=self.__id_column,
                                                    value=user_id,
                                                    columns=columns)
        if not response:
            raise StateError("User was not found")

        state = response[0]
        return state[self.__params_column]

    def is_free(self, user_id: int) -> bool:
        '''
        Checks if user's status is set to "free"

        Parameters
        ----------
        user_id : int
            User's id from the storage

        Returns
        -------
        bool
            wheter user's status if "free" or not
        '''
        user_status = self.get_state(user_id)

        if self.__with_params:
            return True if user_status[self.__status_column] == self.__free_status else False
        else:
            return True if user_status == self.__free_status else False

    def set_state(self, user_id: int, status: str, params: dict = {}) -> None:
        '''
        Set user's status (and user's state_params if with_params = True)

        Parameters
        ----------
        user_id : int
            User's id from the storage
        status : str, dict
            user's status string
        params : dict
            user's state_params (if with_params = True)

        Raises
        ------
        StateError
            Raises an exception if something went wrong trying to change user's status (i.e wrong id)
        '''
        try:
            status_doc = {
                self.__status_column: status
            }

            if self.__with_params:
                status_doc[self.__params_column] = params

            self.__storage.update_one_doc(collection=self.__users_collection,
                                        id_column=self.__id_column,
                                        id=user_id,
                                        doc=status_doc)

        except:
            raise StateError(f'Failed to change {user_id}\'s state to {status}')

    def set_free(self, user_id: int) -> None:
        '''
        Sets user's status to "free" (and state_params to {} if with_params = True)

        Parameters
        ----------
        user_id : int
            User's id from the storage
        '''
        if self.__with_params:
            self.set_state(user_id=user_id,
                        status=self.__free_status,
                        params={})
        else:
            self.set_state(user_id=user_id,
                        status=self.__free_status)
