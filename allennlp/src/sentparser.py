#!/usr/bin/env python
"""
File: sentparser.py
Author: xc383@drexel.edu
Date: 2023-10-3
Purpose: An document parser for knowledge graph construction using the AllenNLP openie model. Will tokenize document into sentences before execution of model.
"""

from sentencizer import Sentencizer
from allennlp.predictors.predictor import Predictor
import allennlp_models.tagging

class SentParser():
    """
    A base text parser class. This implementation parses documents into sentences then executes an AllenNLP predictor.
    :param model_address (str): An AllenNLP model address to intialize with a predictor.
    """

    def __init__(self, model_address: str):
        self.__sentencizer = Sentencizer()
        self.__predictor = Predictor.from_path(model_address)

    def sentencizer(self, doc: str) -> list:
        """
        Tokenize a document into sentences.
        :param doc (str): A document to tokenize.
        :return: A list of sentences.
        """

        return self.__sentencizer.parse(doc)

    def parse(self, doc: str) -> list:
        """
        Will parse a given document and return a each sentence parsed by the AllenNLP model.
        :param doc (str): A document to tokenize and process.
        :ruturns: Returns a list of sentences in the document with model output.
        """
        artifacts = []
        for sent in self.sentencizer(doc):
            artifacts.append(self.__predictor.predict(sentence=sent))

        return artifacts
