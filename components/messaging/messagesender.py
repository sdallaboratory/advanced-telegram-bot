from typing import List

import telegram as tg
import telegram.ext as tg_ext

from ..logs.botlogger import BotLogger


class MessageSender:
    """
    Class that sends messages to users.

    ..........
    Attributes
    ----------
    updater: telegram.ext.Updater, private
        `python-telegram-bot` class, providing a frontend to telegram bot
    logger: BotLogger, private
        logger/logs manager

    .......
    Methods
    -------
    send_text(): public
        sends text message to user
    """
    def __init__(self,
                 updater: tg_ext.Updater,
                 logger: BotLogger) -> None:
        """
        Constructor.

        .........
        Arguments
        ---------
        updater: telegram.ext.Updater, required
            `python-telegram-bot` class, providing a frontend to telegram bot
        logger: BotLogger, required
            logger/logs manager
        """
        self.__updater = updater
        self.__logger = logger

    def send_text(self,
                  user_id: int,
                  text: str,
                  reply_keyboard: List[List[str]] = None,
                  reply_keyboard_resize = True,
                  one_time_keyboard = True) -> None:
        """
        Sends text message to user.

        .........
        Arguments
        ---------
        user_id: int, required
            id of user whom to send message
        text: str, required
            text of sending message
        reply_keyboard: List[List[str]], optional (default = None)
            reply keyboard buttons' texts
        reply_keyboard_resize: bool, optional (default = True)
            flag that requests clients to resize keyboard
        one_time_keyboard: bool, optional (default = True)
            flag that removes older keyboard or hides present one after it is used
        """
        if reply_keyboard is None:
            if one_time_keyboard:
                reply_keyboard = tg.ReplyKeyboardRemove()
        else:
            reply_keyboard = tg.ReplyKeyboardMarkup(keyboard=reply_keyboard,
                                                    resize_keyboard=reply_keyboard_resize,
                                                    one_time_keyboard=one_time_keyboard)

        message = self.__updater.bot.send_message(chat_id=user_id,
                                                  text=text,
                                                  reply_markup=reply_keyboard)
        self.__logger.log_send_msg(id=user_id, text=text)

