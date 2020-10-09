import copy
from typing import Any

from ..utils.filemanager import FileManager


class LocaleManager:
    """
    Class for locale-dependent content loading and managing

    ...
    Attributes
    ---
    locales: dict
        dictionary with locales ("locale_name": <locale>)

    Methods
    ---
    load_locales(): private
        loads all found locales json files from given folder into locales attribute
    load_locale(): private
        loads locale from given path (must be json file)
    get_format_reply(): public
        gets reply with given name which requires formatting
    get_keyboard(): public
        gets keyboard as list of buttons
    get_keyboard_button(): public
        gets button with given name
    get_other() public
        gets other locale-dependent data with given name
    get_simple_reply(): public
        gets reply with given name which does not require formatting
    """
    def __init__(self, locales_folder: str) -> None:
        """
        Arguments:
        ---
        locales_folder: str, required
            path to folder that contains locales json files
        """
        self.__locales = dict()
        self.__load_locales(locales_folder)

    def __load_locales(self, locales_folder: str) -> None:
        """
        Loads all found locales json files from given folder into locales attribute.
        Locale json file must contain key "code" which value is referred to as
        locale argument in public methods

        Arguments
        ---
        locales_folder: str, required
            path to folder that contains locales json files
        """
        for locale_path in FileManager.list_files(locales_folder):
            locale = self.__load_locale(locale_path)
            self.__locales[locale['code']] = locale

    def __load_locale(self, locale_path: str) -> dict:
        """
        Loads locale from given path (must be json file)

        Arguments
        ---
        locale_path: str, required
            path to locale json file
        """
        return FileManager.read_json(locale_path)

    def get_format_reply(self, name: str, locale: str) -> str:
        """
        Gets reply with given name which requires formatting
        Loaded locales must contain key "replies", "format" inside of "replies" value
        and name inside of "format" value

        Arguments
        ---
        name: str, required
            name of reply (which is key of reply inside "format" value)
        locale: str, required
            locale code
        """
        return self.__locales[locale]['replies']['format'][name]

    def get_keyboard(self, name: str, locale: str) -> list:
        """
        Gets keyboard as list of buttons.
        Locale file must contain 'keyboards':'arrangements':'<name>' structure.

        .........
        Arguments
        ---------
        name: str, required
            name of the keyboard
        locale: str, required
            locale code
        """
        buttons = copy.deepcopy(self.__locales[locale]['keyboards']['arrangements'][name])
        for i in range(len(buttons)):
            for j in range(len(buttons[i])):
                buttons[i][j] = self.get_keyboard_button(buttons[i][j], locale)
        return buttons

    def get_keyboard_button(self, button: str, locale: str) -> str:
        """
        Gets button with given name.
        Locale file must contain 'keyboards':'buttons':'<button>' structure.

        .........
        Arguments
        ---------
        button: str, required
            button name
        locale: str, required
            locale code
        """
        return self.__locales[locale]['keyboards']['buttons'][button]

    def get_other(self, name: str, locale: str) -> Any:
        """
        Gets other locale-dependent data with given name
        Loaded locales must contain key "other" and name inside of "replies" value

        Arguments
        ---
        name: str, required
            name of locale-dependent data (which is key inside "other" value)
        locale: str, required
            locale code
        """
        return self.__locales[locale]['other'][name]

    def get_simple_reply(self, name: str, locale: str) -> str:
        """
        Gets reply with given name which does not require formatting
        Loaded locales must contain key "replies", "format" inside of "replies" value
        and name inside of "simple" value

        Arguments
        ---
        name: str, required
            name of reply (which is key of reply inside "simple" value)
        locale: str, required
            locale code
        """
        return self.__locales[locale]['replies']['simple'][name]

