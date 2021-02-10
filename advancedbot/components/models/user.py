from typing import Union
import telegram as tg


class User:
    """
    Model representing bot user

    ..........
    Attrubutes
    ----------
    id: int, public
        telegram user id
    username: str, public
        telegram user username
    first_name: str, public
        telegram user first name
    last_name: str, public
        telegram user last name
    state: Union[str, dict], public
        state of user presented by state name and params (optional)
    roles: List[str], public
        user's roles
    """
    def __init__(self,
                 tg_user: tg.Chat) -> None:
        """
        Constructor.

        .........
        Arguments
        ---------
        tg_user: telegram.Chat
            `python-telegram-bot` class object providing chat info
        """
        self.id: int = tg_user.id
        self.username: str = tg_user.username
        self.first_name: str = tg_user.first_name
        self.last_name: str = tg_user.last_name

        self.roles: list = []
        self.state: Union[str, dict] = None

