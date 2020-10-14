import os
import json

from .storage import Storage, StorageException
from ..utils.datafiltering import DataFiltering


class LocalJSONStorage(Storage):
    '''
    A class used to work with local storage

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
    def __init__(self, storage_folder: str) -> None:
        self.__folder = storage_folder + '/'
        self.__init_storage_folder(self.__folder)

    def __init_storage_folder(self, folder: str):
        if not os.path.exists(folder):
            os.makedirs(folder)

    def __write_data_to_json(self, file_name: str, data: list) -> None:
        with open(file_name, 'w') as data_file:
            json.dump(data, data_file)
            data_file.close()

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
            with open(self.__folder + collection + '.json', 'r') as data_file:
                data = json.load(data_file)
                data_file.close()

            if doc:
                data = filter(lambda x: doc.items() <= x.items(), data)
                data = list(data)

            if columns:
                data = DataFiltering.dict_list_slice(dicts=data,
                                                    columns=columns)
            if count:
                data = data[:count]

            return data
        except:
            raise StorageException("Failed to get data from storage")

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
        column_dict = {
            by: value
        }

        find_res = self.get_data(collection=collection,
                                columns=columns,
                                doc=column_dict,
                                count=count)

        return find_res

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
            try:
                data = self.get_data(collection=collection)
            except:
                data = []

            data.append(doc)

            self.__write_data_to_json(self.__folder + collection + '.json', data)

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
            try:
                data = self.get_data(collection=collection)
            except:
                data = []

            data += docs

            self.__write_data_to_json(self.__folder + collection + '.json', data)

        except:
            raise StorageException('Failed to insert a doc to collection')

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
        self.remove_one_doc_by_dict(collection=collection,
                                    doc={column: value})

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
            count = 0
            data = self.get_data(collection=collection)
            for dic in data:
                try:
                    if doc.items() <= dic.items():
                        count += 1
                        data.remove(dic)
                        break
                except:
                    continue

            self.__write_data_to_json(self.__folder + collection + '.json', data)
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
        self.remove_many_docs_by_dict(collection=collection,
                                    doc={column: value})

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
            count = 0
            data = self.get_data(collection=collection)
            for dic in data.copy():
                try:
                    if doc.items() <= dic.items():
                        data.remove(dic)
                        count += 1
                except:
                    continue

            self.__write_data_to_json(self.__folder + collection + '.json', data)
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
            count = 0
            data = self.get_data(collection=collection)
            for index,_ in enumerate(data):
                try:
                    if data[index][id_column] == id:
                        for key in doc.keys():
                            data[index][key] = doc[key]
                        count += 1
                        break
                except:
                    continue

            if count != 0:
                self.__write_data_to_json(self.__folder + collection + '.json', data)

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
            count = 0
            data = self.get_data(collection=collection)
            for index,_ in enumerate(data):
                try:
                    if data[index][id_column] == id:
                        for key in doc.keys():
                            data[index][key] = doc[key]
                        count += 1
                except:
                    continue
            if count != 0:
                self.__write_data_to_json(self.__folder + collection + '.json', data)
        except:
            raise StorageException('Failed to update a doc from collection!')
