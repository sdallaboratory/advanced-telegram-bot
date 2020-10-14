from abc import ABC, abstractmethod

from .exceptions.storageexception import StorageException


class Storage(ABC):
    '''
    Base class for storing data
    '''
    #---------------------------------------------------------------------------
    # Getting methods
    #---------------------------------------------------------------------------

    @abstractmethod
    def get_data(self, collection: str, columns: list = [], doc: dict = {}, count: int = 0) -> list:
        '''
        Getting list of documents from the certain collection

        Keyword arguments:
        ---
        collection : str, required
            collection name from the storage
        columns : list, optional (default [])
            list of columns to get values from
        '''
        pass

    @abstractmethod
    def get_data_by_column(self, collection: str, by: str, value: str, columns: list = [], count: int = 0) -> list:
        '''
        Getting list of documents from the certain collection by requested column: value

        Keyword arguments:
        ---
        collection : str, required
            collection name from the storage
        columns : list, optional (default [])
            list of columns to get values from
        by: str, required
            column name to search by
        value: str, required
            value from the column
        '''
        pass

    #---------------------------------------------------------------------------
    # Insertion methods
    #---------------------------------------------------------------------------

    @abstractmethod
    def insert_one_doc(self, collection: str, doc: dict) -> None:
        '''
        Inserts document to the collection

        Keyword arguments:
        ---
        collection : str, required
            collection name from the storage
        doc : dict, required
            document to insert to the storage
        '''
        pass

    @abstractmethod
    def insert_many_docs(self, collection: str, docs: list) -> None:
        '''
        Inserts list of documents to the collection

        Keyword arguments:
        ---
        collection : str, required
            collection name from the storage
        docs : list<dict>, required
            listr of documents to insert to the storage
        '''
        pass

    #---------------------------------------------------------------------------
    # Removal methods
    #---------------------------------------------------------------------------

    @abstractmethod
    def remove_one_doc_by_column(self, collection: str, column: str, value: str) -> None:
        '''
        Removes first found document with specified value from the specified column

        Keyword arguments:
        ---
        collection : str, required
            collection name from the storage
        column : str, required
            column name
        value : str, required
            value from the column
        '''
        pass

    @abstractmethod
    def remove_one_doc_by_dict(self, collection: str, doc: dict) -> None:
        '''
        Removes first found document containg values from specified dictionary

        Keyword arguments:
        ---
        collection : str, required
            collection name from the storage
        doc : dict, required
            "collection_column_name - value" dictionary
        '''
        pass

    @abstractmethod
    def remove_many_docs_by_column(self, collection: str, column: str, value: str):
        '''
        Removes all documents with specified value from the specified column

        Keyword arguments:
        ---
        collection : str, required
            collection name from the storage
        column : str, required
            column name
        value : str, required
            value from the column
        '''
        pass

    @abstractmethod
    def remove_many_docs_by_dict(self, collection: str, doc: dict) -> None:
        '''
        Removes all documents containg values from specified dictionary

        Keyword arguments:
        ---
        collection : str, required
            collection name from the storage
        doc : dict, required
            "collection_column_name - value" dictionary
        '''
        pass

    #---------------------------------------------------------------------------
    # Update methods
    #---------------------------------------------------------------------------

    @abstractmethod
    def update_one_doc(self, collection: str, id_column: str, id: str, doc: dict) -> None:
        '''
        Updates first found doc in certain collection by chosen column by dictionary from args

        Keyword arguments:
        ---
        collection : str, required
            collection name from the storage
        id_column : str, required
            name of the id column
        id : str, required
            id value itself
        doc : dict, required
            dictionay with values to update for the found doc by id
        '''
        pass

    @abstractmethod
    def update_many_docs(self, collection: str, id_column: str, id: str, doc: dict) -> None:
        '''
        Updates all documents in certain collection by chosen column by dictionary from args

        Keyword arguments:
        ---
        collection : str, required
            collection name from the storage
        id_column : str, required
            name of the id column
        id : str, required
            id value itself
        doc : dict, required
            dictionay with values to update for every found document by id
        '''
        pass
