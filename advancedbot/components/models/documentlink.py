from typing import Union
import telegram as tg


class DocumentLink:
    def __init__(self,
                 tg_document: Union[tg.Document, tg.File]) -> None:
        self.__tg_document: tg.Document = None
        self.__tg_file: tg.File = None
        self.file_name: str = None

        if type(tg_document) == tg.Document:
            self.__tg_document = tg_document
            self.__tg_file = self.__tg_document.get_file()
            self.file_name = self.__tg_document.file_name
        else:
            self.__tg_file = tg_document

        self.mime_type: self.__tg_file.mime_type
        self.file_size: self.__tg_file.file_size

    def download(self, directory: str, file_name: str = None) -> str:
        if file_name is None:
            file_name = self.file_name

        if !directory.endswith('/'):
            directory += '/'

        download_path: str = directory + file_name
        self.__tg_file.download(custom_path=download_path)

        return download_path

