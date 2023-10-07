#!/usr/bin/env python
"""
File: dirscraper.py
Author: xc383@drexel.edu
Date: 2023-10-3
Purpose: A directory scraper to pull files through a process.
"""

import os

class DirScraper():

    def __init__(self, pull_directory:str, push_directory:str, processor=None):
        self.__pull = os.path.abspath(pull_directory)
        self.__push = os.path.abspath(push_directory)
        self.__processor = processor

        if not self.__validate_pull():
            raise FileNotFoundError("Unable to find pull_directory of '%s'." % self.__pull)
        if not self.__validate_push():
            raise FileNotFoundError("Unable to find push_directory of '%s'." % self.__push)

    def __validate_directory(self, dir: str) -> bool:
        full_dir = os.path.abspath(dir)
        return os.path.exists(full_dir)

    def __validate_pull(self):
        return self.__validate_directory(self.__pull)

    def __validate_push(self):
        return self.__validate_directory(self.__push)

    def __get_pull(self, filter_statement=None):
        for file_name in os.listdir(self.__pull):
            if (filter_statement and filter_statement(file_name)) or (not filter_statement):
                yield {
                    os.path.join(self.__pull, file_name): os.path.join(self.__pull, file_name)
                    }

    def set_processor(self, processor):
        self.__processor = processor

    def process(self, **kwargs):
        for key, item in self.__get_pull():
            with open(item, "r") as fp:
                yield {
                    key: self.__processor(fp.read(), **kwargs)
                }

    def push(self, processed_item: dict, mode:str="w"):
        for key, item in processed_item:
            new_file = os.path.join(self.__push, os.path.basename(key))
            with open(new_file, mode) as fp:
                fp.write(processed_item)
