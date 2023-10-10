#!/usr/bin/env python
"""
File: openie.py
Author: xc383@drexel.edu
Date: 2023-10-3
Purpose: An extractor of triplets for knowledge graph construction using the AllenNLP openie model.
"""

import os
import sys

# Load allennlp directory to path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)

from sentparser import SentParser

OPENIE_MODEL_ADDRESS = "https://storage.googleapis.com/allennlp-public-models/openie-model.2020.03.26.tar.gz"

class OpenIE(SentParser):
    """
    AllenNLP OpenIE implementation.
    """

    def __init__(self):
        super().__init__(OPENIE_MODEL_ADDRESS)