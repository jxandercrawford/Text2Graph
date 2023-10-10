#!/usr/bin/env python
import os
import sys

# Load root directory to path
ROOT_DIR = os.path.abspath(os.getenv("HOME"))
sys.path.append(ROOT_DIR)

import argparse
import json
from tqdm import tqdm

from processor import Document
from text2graph.base.procpipe import ProcPipe
from text2graph.base.xfile import FilePull, FilePush

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
    Run the NLTK pipeline on an mtsample parsing.
    :param document (dict): The mtsample parsing.
    :returns: Parsed document as a dict.
    """
    nlp = Document(document["text"])
    return {
        "type_id": document["type_id"],
        "sample_id": document["sample_id"],
        "sentences": nlp.tokens,
        "pos": nlp.pos
    }

def nlp_processor(path: str) -> str:
    """
    Given a path to a mtsample parsing process it with the NLTK pipeline.
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
        description="Parses mtsamples JSON files with NLTK for tokenization and part-of-speach."
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
