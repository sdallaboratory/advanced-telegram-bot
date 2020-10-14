import time

from ..storage_managing.storage import Storage
from .exceptions.wrongloglevelerror import WrongLogLevelError


class BotLogger:
    """
    Telegram bot logger writing into DB

    ...
    Attributes
    ---
    levels: dict, static
        available log levels enum
    current_level: str
        current log level: messages with levels higher or equal to current are sent
    collection: str
        DB collection name to send logs to
    storage: Storage
        DB wrapper to send or dump logs
    short_params: bool
        one-string log params flag (params are cut if True)

    Methods
    ---
    cut_params(params)
        cuts params values to a single string
    log_cleaning()
        logs cleaning old logs from DB with info level
    write_log(level, event, params)
        sends log to DB with regard to current log level and flag values
    clean_old(min_age)
        deletes logs older than given age
    dump_last(count)
        dumps given count of last sent logs
    log_error(event, params)
        logs given event with error level
    log_receive_command(id, command)
        logs receiving command with info level
    log_receive_document(id, filename)
        logs receiving document with info level
    log_receive_msg(id, text)
        logs receiving message with info level
    log_send_document(id, filename)
        logs sending document with info level
    log_send_msg(id, text)
        logs sending message with info level
    log_start()
        logs starting bot with info level
    log_stop()
        logs stopping bot with info level
    set_level(level)
        sets current log level to given
    """

    levels = {'DEBUG': 1, 'INFO': 2, 'WARNING': 3, 'ERROR': 4, 'CRITICAL': 5}

    def __init__(self,
                 storage: Storage,
                 collection_name: str) -> None:
        """
        Keyword arguments:
        ---
        storage: Storage, required
            DB storage sevice
        collection_name: str
            name of DB collection for logs
        """
        self.__current_level: str = 'INFO'

        self.__collection: str = collection_name
        self.__storage: Storage = storage

        self.short_params: bool = True

    def __cut_params(self, params: dict) -> dict:
        """
        Cuts params values to a single string. If param value contains at least one "\n",
        replacing it with all content afterwards with " <...>".

        Keyword arguments:
        ---
        params: dict, required params which values need to be cut to a single string
        """
        for param in params:
            params[param] = str(params[param])
            if '\n' in params[param]:
                params[param] = params[param].split('\n')[0] + ' <...>'
        return params

    def __log_cleaning(self) -> None:
        """
        Logs cleaning old logs from DB with info level.
        """
        self.__write_log('INFO', 'Old logs cleaned')


    def __write_log(self, level: str, event: str, params: dict = None) -> None:
        """
        Sends log to DB with regard to current log level and flag values.

        Keyword arguments:
        ---
        level: str, required
            level to send log with (if less than current, does not send log)
        event: str, required
            main log description
        params: dict, optional
            additional params to log
        """
        if self.levels[self.__current_level] > self.levels[level]:
            return

        document = {
                    'time': int(time.time() * 1000),
                    'event': event
                   }
        if params:
            if self.short_params:
                params = self.__cut_params(params)
            document['params'] = params

        self.__storage.insert_one_doc(self.__collection, document)


    def clean_old(self, min_age: int) -> None:
        """
        Deletes from DB logs older than given age

        Keyword arguments:
        ---
        min_age: int, required
            minimal age (in milliseconds) to delete logs from
        """
        max_time = int(time.time() * 1000) - min_age
        self.__storage.remove_many_docs_by_dict(self.__collection, {'time': {'$lte': max_time}})
        self.__log_cleaning()

    def dump_last(self, count: int) -> list:
        """
        Dumps from DB given count of last sent logs

        Keyword arguments:
        ---
        count: int, required
            number of logs to dump
        """
        return self.__storage.get_data(self.__collection)[-count:]

    def log_error(self, event: str, params: dict = None) -> None:
        """
        Logs given event with error level.

        Keyword arguments
        ---
        event: str, requrired
            main log description
        params: dict, optional
            additional params to log
        """
        self.__write_log('ERROR', event, params)

    def log_receive_command(self, id: int, command: str) -> None:
        """
        Logs receiving command with info level.

        Keyword arguments
        ---
        id: int, required
            telegram id of user who sent command
        command: str, required
            received command
        """

        self.__write_log('INFO',
                         'Command received',
                         {'id': id, 'command': command})

    def log_receive_document(self, id: int, filename: str) -> None:
        """
        Logs receiving document with info level.

        Keyword arguments
        ---
        id: int, required
            telegram id of user who sent document
        filename: str, required
            filename of received document
        """
        self.__write_log('INFO',
                         'Document received',
                         {'id': id, 'filename': filename})

    def log_receive_msg(self, id: int, text: str) -> None:
        """
        Logs receiving message with info level.

        Keyword arguments
        ---
        id: int, required
            telegram id of user who sent message
        text: str, required
            received message text
        """
        self.__write_log('INFO',
                         'Message received',
                         {'id': id, 'text': text})

    def log_send_document(self, id: int, filename: str) -> None:
        """
        Logs sending document with info level.

        Keyword arguments
        ---
        id: int, required
            telegram id of receipient
        filename: str, required
            sent document filename
        """
        self.__write_log('INFO',
                         'Document sent',
                         {'id': id, 'filename': filename})

    def log_send_msg(self, id: int, text: str) -> None:
        """
        Logs sending message with info level.

        Keyword arguments
        ---
        id: int, required
            telegram id of receipient
        text: str, required
            sent message text
        """
        self.__write_log('INFO',
                         'Message sent',
                         {'id': id, 'text': text})

    def log_start(self) -> None:
        """
        Logs starting bot with info level.
        """
        self.__write_log('INFO',
                         'Bot started')

    def log_stop(self) -> None:
        """
        Logs stopping bot with info level.
        """
        self.__write_log('INFO',
                         'Bot stopped')

    def set_level(self, level: str) -> None:
        """
        Sets current log level to given. If given log level does not exist, exception is raised

        Keyword arguments
        ---
        level: str, required
            log level that current level must be

        Raisable exceptions
        ---
        WrongLogLevelError
            raised if given log level does not exist
        """
        if level in self.levels:
            self.__current_level = level
        else:
            raise WrongLogLevelError(level)

