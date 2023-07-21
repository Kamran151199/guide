
"""
    Wrapper around the default environ module.
"""

import logging
import os
from typing import Union

import dotenv


class Env:
    """
    Wrapper for os.environ.get()
    method with more functionality.
    """

    def __init__(self, path: str):
        """
        Handler for env variables.

        :param path: full path to .env file
        """
        if not os.path.exists(path):
            if not dotenv.find_dotenv(".env"):
                logging.getLogger(__name__).warning(
                    "No .env file found. "
                    "Please create one or system wide env variables will be used."
                )
            path = dotenv.find_dotenv(".env")
        dotenv.load_dotenv(path)

    @staticmethod
    def str_env(name: str, default: str = None):
        """
        Load env variable as string.

        :param name: Key/Name of the env variable
        :param default: Default value of the env variable
        :return: str
        """
        return os.environ.get(name, default)

    @staticmethod
    def int_env(name: str, default: int = 0):
        """
        Load env variable as int.

        :param name: Key/Name of the env variable
        :param default: Default value of the env variable
        :return: int
        """
        return int(os.environ.get(name, default))

    @staticmethod
    def float_env(name: str, default: float = 0.0):
        """
        Load env variable as float.

        :param name: Key/Name of the env variable
        :param default: Default value of the env variable
        :return: float
        """
        return float(os.environ.get(name, default))

    @staticmethod
    def bool_env(name: str, default: Union[bool, int]):
        """
        Load env variable as bool.

        :param name: Key/Name of the env variable
        :param default: Default value of the env variable
        :return: bool
        """
        return bool(int(os.environ.get(name, default)))

    @staticmethod
    def list_env(name: str, separator: str, default: str):
        """
        Load env variable as bool.

        :param name: Key/Name of the env variable
        :param separator: char to separate the list items in string.
        :param default: Default value of the env variable
        :return: bool
        """
        return os.environ.get(name, default).split(separator)
