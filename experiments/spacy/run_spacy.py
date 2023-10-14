#!/usr/bin/env python
import os
import sys

# Load root directory to path
ROOT_DIR = os.path.abspath(os.getenv("HOME"))
sys.path.append(ROOT_DIR)

import argparse
import json
from tqdm import tqdm

from text2graph.base.procpipe import ProcPipe
from text2graph.base.xfile import FilePull, FilePush

import spacy
nlp = spacy.load("en_core_web_sm")

PIPELINE_ACTIONS = ["tok2vec", "tagger", "parser", "ner", "lemmatizer"]

def read_parsed_mtsample(path: str) -> str:
    """
    Read an mtsample parse file.
    :param path (str): Path to file to read.
    :returns: The content of the mtsample parsing.
    """
    with open(path, "r") as file:
        return json.loads(file.read())

def run_nlp_pipeline(document: dict):
    """
    Run the SpaCy pipeline on an mtsample parsing.
    :param document (dict): The mtsample parsing.
    :returns: Parsed document as a dict.
    """
    values = {
        "type_id": document["type_id"],
        "sample_id": document["sample_id"]
    }

    processing_steps = {
        "tok2vec": (lambda doc: [token.vector.tolist() for token in doc]),
        "tagger": (lambda doc: [(token.text, token.tag_) for token in doc]),
        "parser": (lambda doc: [(token.text, token.dep_) for token in doc]),
        "ner": (lambda doc: [(ent.text, ent.label_) for ent in doc.ents]),
        "lemmatizer": (lambda doc: [(token.text, token.lemma_) for token in doc])
    }

    doc = nlp(document["text"])
    for action in PIPELINE_ACTIONS:
        if action in processing_steps:
            values[action] = processing_steps[action](doc)

    return values

def nlp_processor(path: str) -> str:
    """
    Given a path to a mtsample parsing process it with the SpaCy pipeline.
    :param path (str): Path to file to read.
    :returns: The file name and parsed document as a JSON string as a tuple. (name, content)
    """
    content = json.dumps(
        run_nlp_pipeline(
            read_parsed_mtsample(
                path
            )
        )
    )
    return (
        os.path.basename(path),
        content
    )

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Parses mtsamples JSON files with SpaCy for %s." % ", ".join(PIPELINE_ACTIONS)
    )

    parser.add_argument(
        "inpath",
        help="The path to read in the mtsample JSON. Expects files to be named 'mtsamples-type-$TYPE-sample-$SAMPLE_NUMBER.json'",
        type=str
    )

    parser.add_argument(
        "outpath",
        help="Optional. The path write the mtsamples JSON files. Defaults to '%s'." % os.getcwd(),
        type=str,
        default=os.getcwd()
    )

    args = parser.parse_args()
    pull = FilePull(args.inpath)
    push = FilePush(args.outpath)

    pipe = ProcPipe(pull, push, nlp_processor)

    process = pipe.run()

    for _ in tqdm(process, desc="Processing documents", unit=" doc"):
        pass