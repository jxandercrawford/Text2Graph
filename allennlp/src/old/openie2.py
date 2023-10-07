#!/usr/bin/env python
"""
File: extractor.py
Author: xc383@drexel.edu
Date: 2023-9-30
Purpose: An extractor of triplets for knowledge graph construction using the AllenNLP openie model.
"""

from nltk.tokenize import sent_tokenize
from allennlp.predictors.predictor import Predictor
import allennlp_models.tagging

OPENIE_MODEL_ADDRESS = "https://storage.googleapis.com/allennlp-public-models/openie-model.2020.03.26.tar.gz"

class Extractor():
    """
    A text parser that extracts triplets of (subject, predicate, object) using the AllenNLP openie model.
    """

    def __init__(self):
        self.__predictor = Predictor.from_path(OPENIE_MODEL_ADDRESS)

    def sentencizer(self, doc: str) -> list:
        """
        Tokenize a document into sentences.
        :param doc (str): A document to tokenize.
        :return: A list of sentences.
        """

        return sent_tokenize(doc)

    def parse(self, doc: str) -> list:
        """
        Will parse a given document and return a list of triplets.
        :param doc (str): A document to tokenize.
        :ruturns: Returns a list of sentences in the document with their triplets extracted.
        """
        artifacts = []
        for sent in self.sentencizer(doc):
            artifacts.append(self.__predictor.predict(sentence=sent))

        return artifacts
