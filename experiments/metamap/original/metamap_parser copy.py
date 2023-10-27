#!/usr/bin/env python
"""
File: metamap_parser.py
Author: xc383@drexel.edu
Date: 2023-10-18
Purpose: A parser for metamap JSONs.
"""

import argparse
import os
import json
from tqdm import tqdm
from dataclasses import fields
from typing import Any
import csv
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))     # For modules within this experiment
ROOT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))     # For modules within this project
sys.path.append(BASE_DIR)
sys.path.append(ROOT_DIR)

from base.xfile import FilePull
from base.procpipe import ProcPipe
from mapping import Mapping, map_to_uterance

JSON_PATH_TO_DATA = ["AllDocuments", "Document", "Utterances", "Phrases", "Mappings", "MappingCandidates"]
OUTFILE_NAME = "metamap_mappings.csv"

def failproof(func, default=None, verbose:bool=False):
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if verbose:
                print(e)
            return default
    return wrap

from typing import Any

def flatten(lists: list[list[Any]]) -> list[Any]:
    """
    Will flatten a list into a single list.
    :param lists (list[list[Any]]): A list of lists.
    :returns: A list.
    """
    flat = []
    for xs in lists:
        flat += xs
    return flat

def crawl(mapping, keyset, func=lambda x: x):

    content = []
    key = keyset[0]
    value = mapping.get(key)

    if not keyset[1:] and isinstance(value, list):
        for item in value:
            content.append(func(item))
    elif not keyset[1:] and value:
        content.append(func(value))
    elif keyset[1:] and isinstance(value, list):
        for item in value:
            content += crawl(item, keyset[1:], func)
    elif keyset[1:] and isinstance(value, dict):
        content += crawl(value, keyset[1:], func)

    return content

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Parses Metamap output JSON files into a CSV of mappings."
    )

    parser.add_argument(
        "inpath",
        help="The path to read in the Metamap Output JSON(s).",
        type=str
    )

    parser.add_argument(
        "outpath",
        help="The path to write the outputed CSV file. Will create file named %s." % OUTFILE_NAME,
        type=str
    )

    args = parser.parse_args()

    # Read directory for all json files
    pull = FilePull(args.inpath)
    files = pull.pull(filter_statement=lambda x: x[-4:].lower() == "json")

    # Prepare outfile
    outfile = open(os.path.join(args.outpath, OUTFILE_NAME), "w")
    csv_fields = ["file", *map(lambda x: x.name, fields(Mapping))]
    csvfile = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC)
    csvfile.writerow(csv_fields)

    # Failproof the parsing function
    func = failproof(map_to_uterance, [], True)

    # Loop over directory
    for path in tqdm(files, desc="Parsing docs", unit=" doc"):

        # Open file and find start of json
        with open(path, "r") as file:
            lines = file.readlines()
            if lines[0][0] == "{":
                data = json.loads(lines[0])
            else:
                data = json.loads(lines[1])

        # Pull all mappings and write them
        mappings = flatten(crawl(data, JSON_PATH_TO_DATA, func))
        for item in mappings:
            csvfile.writerow([os.path.basename(path), *item.astuple()])

    outfile.close()
