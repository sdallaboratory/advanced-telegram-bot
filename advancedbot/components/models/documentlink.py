from typing import Union
import telegram as tg


class DocumentLink:
    """
    Model representing link to a downloadable document

    ..........
    Attrubutes
    ----------
    name: str, public
        name of document (with extensinon)
    media_group_id: int, public
        telegram id of group of files
    mime_type: str, public
        MIME-type of document
    size: int, public
        size of document (in bytes)
    tg_document: telegram.Document, private
        `python-telegram-bot` class object providing document info
    tg_file: telegram.File, private
        `python-telegram-bot` class object providing download ability
    """
    def __init__(self,
                 tg_document: Union[tg.Document, tg.File],
                 media_group_id: int = None) -> None:
        """
        Constructor.

        .........
        Arguments
        ---------
        tg_document: Union[telegram.Document, telegram.File], required
            `python-telegram-bot` class object providing document info
        media_group_id: int, optional (default is None)
            telegram id of group of files
        """
        self.__tg_document: tg.Document = None
        self.__tg_file: tg.File = None
        self.name: str = None
        self.mime_type: str = None
        self.media_group_id: int = media_group_id

        if type(tg_document) == tg.Document:
            self.__tg_document = tg_document
            self.__tg_file = self.__tg_document.get_file()
            self.name = self.__tg_document.file_name
            self.mime_type = self.__tg_document.mime_type
        else:
            self.__tg_file = tg_document

        self.size: str = self.__tg_file.file_size

    def download(self, directory: str, name: str = None) -> str:
        """
        Constructor.

        .........
        Arguments
        ---------
        directory: str, required
            directory where to save downloaded file
        name: str, optional (default is None)
            name with which to save downloaded file
            if None, self name is given

        Returns
        ------
        str
            path where document has been downloaded
        """
        if name is None:
            name = self.name

        if not directory.endswith('/'):
            directory += '/'

        download_path: str = directory + name
        self.__tg_file.download(custom_path=download_path)

        return download_path

