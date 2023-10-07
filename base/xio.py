#!/usr/bin/env python

from abc import abstractclassmethod
import os

class IO:
    """
    Base IO source class for passing data.
    """

    @abstractclassmethod
    def __self__(self):
        pass

    @abstractclassmethod
    def __validate(self) -> bool:
        """
        Validate that the source exists.
        :returns True if exists and false otherwise.
        """
        pass

class Pull(IO):

    @abstractclassmethod
    def __init__(self):
        pass

    @abstractclassmethod
    def __validate(self) -> bool:
        pass

    @abstractclassmethod
    def pull(self):
        pass

class Push(IO):

    @abstractclassmethod
    def __init__(self):
        pass

    @abstractclassmethod
    def __validate(self) -> bool:
        pass

    @abstractclassmethod
    def push(self):
        pass
