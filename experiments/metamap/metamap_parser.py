#!/usr/bin/env python
"""
File: metamap_parser.py
Author: xc383@drexel.edu
Date: 2023-10-27
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
from metaparse import process_metamap_json
from concept import dict_to_concept, Concept

OUTFILE_NAME = "metamap_concepts.csv"

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

    parser.add_argument(
        "-i", "--ignore",
        help="Flag to ignore errors while parsing. Will print errors to stdout.",
        action="store_true"
    )

    args = parser.parse_args()

    # Read directory for all json files
    pull = FilePull(args.inpath)
    files = pull.pull(filter_statement=lambda x: x[-4:].lower() == "json")

    # Prepare outfile
    outfile = open(os.path.join(args.outpath, OUTFILE_NAME), "w")
    csv_fields = ["file", *map(lambda x: x.name, fields(Concept))]
    csvfile = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC)
    csvfile.writerow(csv_fields)

    # Loop over directory
    for path in files:

        try:
            # Open file and find start of json
            with open(path, "r") as file:
                lines = file.readlines()
                if lines[0][0] == "{":
                    data = json.loads(lines[0])
                else:
                    data = json.loads(lines[1])
        except Exception as e:
            if args.ignore:
                print("\nError while parsing '%s': %s" % (path, e), file=sys.stderr)
            else:
                raise Exception("Error while parsing '%s': %s" % (path, e))

        # Pull all mappings and write them
        concepts = map(dict_to_concept, process_metamap_json(data))
        for item in concepts:
            csvfile.writerow([os.path.basename(path), *item.astuple()])

    outfile.close()
