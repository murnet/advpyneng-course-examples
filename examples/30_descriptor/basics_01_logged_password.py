import logging
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="{msg}",
    style="{",
    handlers=[RichHandler(show_path=False)],
)



class LoggedPasswdAccess:
    def __get__(self, instance, cls=None):
        print(f"__get__ {instance=} {cls=}")
        value = instance._password
        logging.info(f"Read password")
        return value

    def __set__(self, instance, value):
        print(f"__set__ {instance=} {value=}")
        logging.info(f"Write password {value=}")
        instance._password = value


class User:
    password = LoggedPasswdAccess()

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<{type(self).__name__} username={self.username}>"
