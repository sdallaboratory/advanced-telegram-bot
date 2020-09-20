import os

from pymongo import MongoClient

from .storage import Storage, StorageException
from ..utils.datafiltering import DataFiltering


class MongoDBStorage(Storage):
    '''
    A class used to work with MongoDB

    ...
    Attributes
    ---
    address: str
        adress of your mongodb server
    port: int
        port of your mongodb server
    database: str
        name of your database with collections
    collection : str
        collection name from the database
    columns : list
        list of columns to get values from
    doc : dict
        document to insert to the database
    docs : list<dict>
        listr of documents to insert to the database
    value : str
        value from the column
    id_column : str
        name of the id column
    id : str
        id value itself

    Methods
    ---
    get_data(collection, columns)
        Getting list of documents from the certain collection
    get_data_by_column(collection, by, value, columns)
        Getting list of documents from the certain collection by requested column: value
    insert_one_doc(collection, doc)
        Inserts document to the collection
    insert_many_docs(collection, docs)
        Inserts list of documents to the collection
    remove_one_doc_by_column(collection, column, value)
        Removes first found document with specified value from the specified column
    remove_many_docs_by_column(collection, column, value)
        Removes all documents with specified value from the specified column
    update_one_doc(collection, id_column, id, doc)
        Updates first found doc in certain collection by chosen column by dictionary from args
    update_many_docs(collection, id_column, id, doc)
        Updates all documents in certain collection by chosen column by dictionary from args
    '''
    def __init__(self,
                address: str = "localhost",
                port: int = 27017,
                username: str = "",
                password: str = "",
                database: str = "config"):
        '''
        Keyword arguments:
        ---
        address: str, optional (default "localhost")
            adress of your mongodb server
        port: int, optional (default 27017)
            port of your mongodb server
        database: str, optional (default "config")
            name of your database name with collection
        '''
        self.__init_mongo_connection(address=address,
                                    port=port,
                                    username=username,
                                    password=password)
        self.__database = self.__client[database]

    def __init_mongo_connection(self, address: int, port: int, username: str, password: str) -> None:
        try:
            self.__client = MongoClient(address, port,
                                        username=username,
                                        password=password)

        except:
            raise StorageException('Failed to connect to mongo!')

    #---------------------------------------------------------------------------
    # Getting methods
    #---------------------------------------------------------------------------

    def get_data(self, collection: str, columns: list = [], doc: dict = {}, count: int = 0) -> list:
        '''
        Getting list of documents from the certain collection

        Keyword arguments:
        ---
        collection : str, required
            collection name from the database
        columns : list, optional (default [])
            list of columns to get values from
        '''

        try:
            db_collection = self.__database[collection]

            if count:
                db_data = list(db_collection.find(doc).limit(count))
            else:
                db_data = list(db_collection.find(doc))

            db_data_filtered = DataFiltering.dict_list_slice(dicts=db_data,
                                                                columns=columns)

            return db_data_filtered
        except:
            raise StorageException('Failed to get data from storage')

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
        try:
            db_collection = self.__database[collection]

            if count:
                db_data = list(db_collection.find({by: value}))
            else:
                db_data = list(db_collection.find({by: value}).limit(count))

            db_data_filtered = DataFiltering.dict_list_slice(dicts=db_data,
                                                                columns=columns)

            return db_data_filtered
        except:
            raise StorageException('Failed to get data from storage')

    #---------------------------------------------------------------------------
    # Insertion methods
    #---------------------------------------------------------------------------

    def insert_one_doc(self, collection: str, doc: dict) -> None:
        '''
        Inserts document to the collection

        Keyword arguments:
        ---
        collection : str, required
            collection name from the database
        doc : dict, required
            document to insert to the database
        '''
        try:
            res = self.__database[collection].insert_one(doc)
        except:
            raise StorageException('Failed to insert a doc to collection')

    def insert_many_docs(self, collection: str, docs: list) -> None:
        '''
        Inserts list of documents to the collection

        Keyword arguments:
        ---
        collection : str, required
            collection name from the database
        docs : list<dict>, required
            listr of documents to insert to the database
        '''
        try:
            res = self.__database[collection].insert_many(docs)
        except:
            raise StorageException('Failed to insert docs to collection!')

    #---------------------------------------------------------------------------
    # Removal methods
    #---------------------------------------------------------------------------

    def remove_one_doc_by_column(self, collection: str, column: str, value: str) -> None:
        '''
        Removes first found document with specified value from the specified column

        Keyword arguments:
        ---
        collection : str, required
            collection name from the database
        column : str, required
            column name
        value : str, required
            value from the column
        '''
        try:
            res = self.__database[collection].delete_one({column: value})
        except:
            raise StorageException('Failed to remove a doc from collection!')

    def remove_one_doc_by_dict(self, collection: str, doc: dict) -> None:
        '''
        Removes first found document containg values from specified dictionary

        Keyword arguments:
        ---
        collection : str, required
            collection name from the database
        doc : dict, required
            "collection_column_name - value" dictionary
        '''
        try:
            res = self.__database[collection].delete_one(doc)
        except:
            raise StorageException('Failed to remove a doc from collection!')

    def remove_many_docs_by_column(self, collection: str, column: str, value: str):
        '''
        Removes all documents with specified value from the specified column

        Keyword arguments:
        ---
        collection : str, required
            collection name from the database
        column : str, required
            column name
        value : str, required
            value from the column
        '''
        try:
            res = self.__database[collection].delete_many({column: value})
        except:
            raise StorageException('Failed to remove a doc from collection!')

    def remove_many_docs_by_dict(self, collection: str, doc: dict) -> None:
        '''
        Removes all documents containg values from specified dictionary

        Keyword arguments:
        ---
        collection : str, required
            collection name from the database
        doc : dict, required
            "collection_column_name - value" dictionary
        '''
        try:
            res = self.__database[collection].delete_many(doc)
        except:
            raise StorageException('Failed to remove a doc from collection!')

    #---------------------------------------------------------------------------
    # Update methods
    #---------------------------------------------------------------------------

    def update_one_doc(self, collection: str, id_column: str, id: str, doc: dict) -> None:
        '''
        Updates first found doc in certain collection by chosen column by dictionary from args

        Keyword arguments:
        ---
        collection : str, required
            collection name from the database
        id_column : str, required
            name of the id column
        id : str, required
            id value itself
        doc : dict, required
            dictionay with values to update for the found doc by id
        '''
        try:
            res = self.__database[collection].update_one({id_column: id}, {'$set': doc}, upsert=True)
        except:
            raise StorageException('Failed to update a doc from collection!')

    def update_many_docs(self, collection: str, id_column: str, id: str, doc: dict) -> None:
        '''
        Updates all documents in certain collection by chosen column by dictionary from args

        Keyword arguments:
        ---
        collection : str, required
            collection name from the database
        id_column : str, required
            name of the id column
        id : str, required
            id value itself
        doc : dict, required
            dictionay with values to update for every found document by id
        '''
        try:
            res = self.__database[collection].update_many({id_column: id}, {'$set': doc}, upsert=True)
        except:
            raise StorageException('Failed to update a doc from collection!')

