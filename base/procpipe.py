#!/usr/bin/env python
"""
File: procpipe.py
Author: xc383@drexel.edu
Date: 2023-10-7
Purpose: Process pipeline implementation utilizing xio.Pull and xio.Push.
"""

import os
import sys

# Load root directory to path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)

from xio import Pull, Push

class ProcPipe():
    """
    Runs a process from end to end in a generator.
    :param pull (Pull): A pull data source.
    :param push (Push): A push data sink.
    :param processor (func): A function to process data from the source. Must accept the Pull output and return the Push input
        - Pull = () => A
        - Push = (B) => C
        - processor = (A) => B
        - ProcPipe = () => C
    :returns: A ProcPipe.
    """

    def __init__(self, pull:Pull, push:Push, processor):
        self.__pull = pull
        self.__push = push
        self.__processor = processor

    def process(self):
        """
        Process items from the pull.
        :returns: A generator of the processor output.
        """
        for item in self.__pull.pull():
            yield self.__processor(item)

    def run(self):
        """
        Run the process from read to process to write.
        :returns: A generator for each item in the process. Will generate push output.
        """
        return self.__push.push(self.process())
