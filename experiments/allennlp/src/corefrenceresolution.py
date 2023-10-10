
import os
import sys

# Load allennlp directory to path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)

COREF_MODEL_ADDRESS = "https://storage.googleapis.com/allennlp-public-models/coref-spanbert-large-2021.03.10.tar.gz"

from docparser import DocParser

class CoreferenceResolution(DocParser):

    def __init__(self):
        super().__init__(COREF_MODEL_ADDRESS)
