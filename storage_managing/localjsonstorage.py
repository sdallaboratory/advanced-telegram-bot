from storage_managing.storage import Storage, StorageException
from utils.datafiltering import DataFiltering

import os
import json


class LocalJSONStorage(Storage):
    def __init__(self, storage_folder: str):
        self.__folder = storage_folder + '/'

    def __init_storage_folder(self, folder: str):
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f'{folder} was successfully initialized!')
        else:
            print(f'{folder} already exists!')

    #---------------------------------------------------------------------------
    # Getting methods
    #---------------------------------------------------------------------------
    
    def get_data(self, collection: str, columns: list = [], doc: dict = {}, count: int = 0) -> list:
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
        try:
            try:
                data = self.get_data(collection=collection)
            except:
                data = []
            
            data.append(doc)

            with open(self.__folder + collection + '.json', 'w') as data_file:
                json.dump(data, data_file)
                data_file.close()

        except:
            raise StorageException('Failed to insert a doc to collection')

    def insert_many_docs(self, collection: str, docs: list) -> None:
        try:
            try:
                data = self.get_data(collection=collection)
            except:
                data = []
            
            data += docs

            with open(self.__folder + collection + '.json', 'w') as data_file:
                json.dump(data, data_file)
                data_file.close()

        except:
            raise StorageException('Failed to insert a doc to collection')

    #---------------------------------------------------------------------------
    # Removal methods
    #---------------------------------------------------------------------------
    
    def remove_one_doc_by_column(self, collection: str, column: str, value: str) -> None:
        pass

    def remove_one_doc_by_dict(self, collection: str, doc: dict) -> None:
        pass

    def remove_many_docs_by_column(self, collection: str, column: str, value: str):
        pass

    def remove_many_docs_by_dict(self, collection: str, doc: dict) -> None:
        pass

    #---------------------------------------------------------------------------
    # Update methods
    #---------------------------------------------------------------------------

    def update_one_doc(self, collection: str, id_column: str, id: str, doc: dict) -> None:
        pass

    def update_many_docs(self, collection: str, id_column: str, id: str, doc: dict) -> None:
        pass

