#!/usr/bin/env python
"""
File: sentencizer.py
Author: xc383@drexel.edu
Date: 2023-10-3
Purpose: A sentence tokenizer to be used with other models that require sentence tokenization. Currently uses nltk's sent_tokenizer.
"""

from nltk.tokenize import sent_tokenize

class Sentencizer():
    """
    A sentence tokenizer.
    """

    def __init__(self):
        pass
    
    def parse(self, doc:str) -> list:
        """
        Tokenize a document into sentences.
        :param doc (str): A document to tokenize.
        :return: A list of sentences.
        """

        return sent_tokenize(doc)