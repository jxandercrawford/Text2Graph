#!/usr/bin/env python

"""
File: mtsample_json_parser.py
Author: xc383@drexel.edu
Date: 2023-10-3
Purpose: A script to read a directory full of mtsamples text files and write them into JSONs.
"""

import argparse
import os
import json
import re
from tqdm import tqdm

BATCH_SIZE = 100

import re

def parse_mtsample(file_name: str, text: str) -> dict:
    """
    Will parse a mtsample file into a dictionary containing content and metadata.
    :param file_name (str): The name of the mtsample file.
    :param text (str): The textual content of the mtsample file.
    :returns: A dictionary of the schema: ```
        {
            type_id: int,
            sample_id: int,
            type: str,
            name: str,
            description: str
            text: str
        }
    ```
    """

    patterns = {
        "file_name": {
            "type_id": "mtsamples-type-(\\d+)-sample-\\d+\\.txt",
            "sample_id": "mtsamples-type-\\d+-sample-(\\d+)\\.txt"
        },
        "text": {
            "type": "Sample Type / Medical Specialty:\\s*([\\w\\s/]+)\n",
            "name": "Sample Name:\\s*([\\w\\s\\-]+)\n",
            "description": "Description:\\s([\\w\\s]+)",
            "text": "\\-{5}\\s*(.*)"
        }
    }

    int_keys = ["type_id", "sample_id"]

    doc = {}

    # Parse file name
    for name, pattern in patterns["file_name"].items():
        # REF: https://stackoverflow.com/questions/587345/regular-expression-matching-a-multiline-block-of-text
        compat = re.compile(pattern, re.MULTILINE|re.DOTALL)
        results = re.search(compat, file_name)
        if results:
            doc[name] = results.groups()[0].strip()
        else:
            doc[name] = None

    # Parse text
    for name, pattern in patterns["text"].items():
        # REF: https://stackoverflow.com/questions/587345/regular-expression-matching-a-multiline-block-of-text
        compat = re.compile(pattern, re.MULTILINE|re.DOTALL)
        results = re.search(compat, text)
        if results:
            doc[name] = results.groups()[0].strip()
        else:
            doc[name] = None

    # Convert types to ints
    for key in int_keys:
        doc[key] = int(doc[key])

    return doc

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Parses mtsamples files into JSON files."
    )

    parser.add_argument(
        "inpath",
        help="The path to read in the mtsamples. Expects files to be named 'mtsamples-type-$TYPE-sample-$SAMPLE_NUMBER.txt'",
        type=str
    )

    parser.add_argument(
        "outpath",
        help="Optional. The path write the mtsamples JSON files. Defaults to '%s'." % os.getcwd(),
        type=str,
        default=os.getcwd()
    )

    args = parser.parse_args()

    inpath = os.path.abspath(args.inpath)
    if not os.path.exists(inpath):
        raise FileNotFoundError("The inpath of '%s' could not be found." % inpath)

    outpath = os.path.abspath(args.outpath)
    if not os.path.exists(outpath):
        raise FileNotFoundError("The outpath of '%s' could not be found." % outpath)
    
    # Parse and write files.
    for file_name in tqdm(os.listdir(inpath), desc="Writing documents", unit=" doc"):
        with open(os.path.join(inpath, file_name), "r", encoding="latin-1") as fp:
            doc = parse_mtsample(file_name, fp.read())

        new_file_name = "." .join(file_name.split(".")[:-1]) + ".json"
        with open(os.path.join(outpath, new_file_name), "w") as fp:
            fp.write(json.dumps(doc))
