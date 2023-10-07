#!/usr/bin/env python
"""
File: docparser.py
Author: xc383@drexel.edu
Date: 2023-10-3
Purpose: 
"""

from allennlp.predictors.predictor import Predictor
import allennlp_models.tagging

class DocParser():
    """
    A base text parser class. This implementation executes an AllenNLP predictor on an entire document.
    :param model_address (str): An AllenNLP model address to intialize with a predictor.
    """

    def __init__(self, model_address: str):
        self.__predictor = Predictor.from_path(model_address)

    def parse(self, doc: str) -> list:
        """
        Will parse a given document.
        :param doc (str): A document to parse.
        :ruturns: Returns a document parsed by the AllenNLP model.
        """
        return self.__predictor.predict(doc)
