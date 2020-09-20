from .botloggererror import BotLoggerError


class WrongLogLevelError(BotLoggerError):
    """
    Wrong log level exception.

    ...
    Attributes
    ---
    level: str
        inputted log level that does not exist
    """

    def __init__(self, wrong_level: str) -> None:
        """
        Keyword arguments:
        ---
        wrong_level: str, required
            inputted log level that does not exist
        """
        self.level = wrong_level

