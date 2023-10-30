#!/usr/bin/env python
"""
File: ctakes_parser.py
Author: xc383@drexel.edu
Date: 2023-10-18
Purpose: A parser for ctakes XMIs.
"""

import argparse
import os
import csv
from dataclasses import fields
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))     # For modules within this experiment
ROOT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))     # For modules within this project
sys.path.append(BASE_DIR)
sys.path.append(ROOT_DIR)

from base.xfile import FilePull
from document import Document
from xml_tools import to_records
from ctakes_model_tools import get_mentions, dict_to_mention
from ctakes_model import Mention

OUTFILE_NAME = "ctake_concepts.csv"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Parses cTakes output XMI files into a CSV of concepts."
    )

    parser.add_argument(
        "inpath",
        help="The path to read in the cTakes Output XMI(s).",
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
    files = pull.pull(filter_statement=lambda x: x[-3:].lower() == "xmi")

    # Prepare outfile
    outfile = open(os.path.join(args.outpath, OUTFILE_NAME), "w")
    fields = ["file", "start", "end", "subject", "polarity", "uncertainty", "confidence", "conditional", "generic", "history", "concept_scheme", "concept_cui", "concept_tui", "concept_text", "concept_score", "concept_disambiguated"]
    csvfile = csv.DictWriter(outfile, quoting=csv.QUOTE_NONNUMERIC, fieldnames=fields)
    csvfile.writeheader()

    # Loop over directory
    for path in files:

        try:
            doc = Document(path)

            for item in map(lambda x: dict_to_mention(x).asdict(flatten=True), get_mentions(doc)):
                item["file"] = os.path.basename(path)
                csvfile.writerow(item)
        except Exception as e:
            if args.ignore:
                print("\nError while parsing '%s': %s" % (path, e), file=sys.stderr)
            else:
                raise Exception("Error while parsing '%s': %s" % (path, e))
    outfile.close()
