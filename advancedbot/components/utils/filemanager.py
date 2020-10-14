import json
import os
from typing import List, Union


class FileManager:
    """
    Static auxiliary  class to simplify data processing

    ..........
    Attributes
    encoding: str, public
        encoding to open files with

    .......
    Methods
    -------
    clean_file(file_path)
        removes all data from given file
    copy_content(src_path, dest_path)
        if src exists, copies its data into dest
    file_exists(file_path)
        checks if given file exists
    get_dir(file_path)
        returns directory path of given file
    is_file(path)
        checks if given path belongs to file
    list_files(dir_path)
        lists all files in given dir (not recursively)
    make_dir(dir_path)
        creates directory with given path
    make_file(file_path)
        creates file with given path
    move_content(src_path, dest_path)
        if src exists, moves its data into dest
    read_json(file_path)
        reads given json file and returns its content
    remove_file(file_path)
        removes given file
    """

    encoding = "utf-8"

    @staticmethod
    def clean_file(file_path: str) -> None:
        """
        Removes all data from given file. File must exist.

        Arguments
        ---
        file_path: str, required
            path of file to clean
        """
        open(file_path, 'w').close()

    @staticmethod
    def copy_content(src_path: str, dest_path: str) -> None:
        """
        If src exists, copites its data into dest.
        If there is data in dest, it will be replaced with new data.

        Arguments
        ---
        src_path: str, required
            path of source file
        dest_path: str, required
            path of destination file
        """
        if not FileManager.file_exists(src_path):
            return

        with open(src_path, 'r') as src_fd:
            with open(dest_path, 'w') as dest_fd:
                dest_fd.writelines(src_fd.readlines())

    @staticmethod
    def file_exists(file_path: str) -> bool:
        """
        Checks if given file exists.

        Arguments
        ---
        file_path: str, required
            path of file to check
        """
        return os.path.exists(file_path)

    @staticmethod
    def get_dir(file_path: str) -> str:
        """
        Returns directory path of given file. File must exist.

        Arguments
        ---
        file_path: str, required
            path of file to get directory path of
        """
        return os.path.dirname(file_path)

    @staticmethod
    def is_file(path: str) -> bool:
        """
        Checks if given path belongs to file

        Arguments
        ---
        path: str, required
            path to check
        """
        return os.path.isfile(path)

    @staticmethod
    def list_files(dir_path: str) -> List[str]:
        """
        Lists all files in given directory (not recursively). Full path list is returned.

        Arguments
        ---
        dir_path: str, required
            path of directory to list files from
        """
        return [dir_path + '/' + content for content in os.listdir(dir_path)\
            if FileManager.is_file(dir_path + '/' + content)]

    @staticmethod
    def make_dir(dir_path: str) -> None:
        """
        Creates directory with given path. If directory exists nothing happens.

        Arguments
        ---
        dir_path: str, required
            path of directory to make
        """
        os.makedirs(dir_path, exist_ok=True)

    @staticmethod
    def make_file(file_path: str) -> None:
        """
        Creates file with given path. If file already exists nothing happens.

        Arguments
        ---
        file_path: str, required
            path of file to make
        """
        dir_path = FileManager.get_dir(file_path)
        if dir_path:
            FileManager.make_dir(dir_path)
        open(file_path, 'a').close()

    @staticmethod
    def move_content(src_path: str, dest_path: str) -> None:
        """
        If src exists, moves its data into dest.
        If dest contains any data, it will be replaced by new data.

        Arguments
        ---
        src_path: str, required
            path of source file
        dest_path: str, required
            path of destonation file
        """
        FileManager.copy_content(src_path, dest_path)
        FileManager.clean_file(src_path)

    @staticmethod
    def read_json(file_path: str) -> Union[list, dict, None]:
        """
        Reads given json file and returns its content. In case of error returns None.

        Arguments
        ---
        file_path: str, required
            path of json file to read
        """
        if not FileManager.file_exists(file_path):
            return
        with open(file_path, 'r', encoding=FileManager.encoding) as fd:
            try:
                return json.load(fd)
            except Exception as e:
                return

    @staticmethod
    def remove_file(file_path: str) -> None:
        """
        Removes given file. If file does not exist, nothing happens.

        Arguments
        ---
        file_path: str, required
            path of file to remove
        """
        if FileManager.file_exists(file_path):
            os.remove(file_path)

