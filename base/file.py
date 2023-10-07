#!/usr/bin/env python

import os
import sys

# Load root directory to path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)

from xio import Pull, Push

class FilePull(Pull):

    def __init__(self, path: str):
        self.__path = path
        self.__full_path = os.path.abspath(path)

        if not self.__validate():
            raise FileNotFoundError("The pull path of '%s' could not be found." % self.__path)

    def __validate(self) -> bool:
        return os.path.exists(self.__full_path)

    def __listdir(self, path: str):
        files = []
        for file in os.listdir(path):
            files.append(os.path.join(path, file))

        return files

    def pull(self, recursive=False, filter_statement=lambda x: True):
        """
        A generator for retrieveing file paths within the source.
        :param recursive (bool): Wether to recursivly pull files from sources subdirectories. Defaults to False.
        :param filter_statement ( (str) => bool ): A filter function that takes the path and returns a bool. Mainly for excluding directories. Defaults to True.
        :returns: Next file path from the source.
        """
        files = []
        if os.path.isfile(self.__full_path):
            # If the full_path is a file than it does not need have anything appended in the loop.
            files.append(self.__full_path)
        else:
            files += self.__listdir(self.__full_path)

        while files:
            file_name = files.pop(0)

            if recursive and os.path.isdir(file_name) and filter_statement(file_name): 
                files += self.__listdir(file_name)
            elif os.path.isfile(file_name) and filter_statement(file_name):
                yield file_name

class FilePush(Pull):

    def __init__(self, path: str):
        self.__path = path
        self.__full_path = os.path.abspath(path)

        if not self.__validate():
            raise FileNotFoundError("The pull path of '%s' could not be found." % self.__path)

    def __validate(self) -> bool:
        return os.path.exists(self.__full_path)

    def push(self):
        pass
