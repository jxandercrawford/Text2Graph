#!/usr/bin/env python
"""
File: semanticrolelabel.py
Author: xc383@drexel.edu
Date: 2023-10-3
Purpose: An extractor of triplets for knowledge graph construction using the AllenNLP semantic role label model.
"""

import os
import sys

# Load allennlp directory to path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)

from sentparser import SentParser

SRL_MODEL_ADDRESS = "https://storage.googleapis.com/allennlp-public-models/structured-prediction-srl-bert.2020.12.15.tar.gz"

class SemanticRoleLabel(SentParser):
    """
    AllenNLP Semantic Role Label implementation.
    """

    def __init__(self):
        super().__init__(SRL_MODEL_ADDRESS)