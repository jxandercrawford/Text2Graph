#!/usr/bin/env python
"""
File: get_ctakes_concepts.py
Author: xc383@drexel.edu
Date: 2023-10-18
Purpose: A parser for ctakes XMIs.
"""

import argparse
import os
from tqdm import tqdm
import csv
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))     # For modules within this experiment
ROOT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))     # For modules within this project
sys.path.append(BASE_DIR)
sys.path.append(ROOT_DIR)

from base.xfile import FilePull
from document import Document
from xml_tools import to_records

OUTFILE_NAME = "ctake_concepts.csv"

# TO REMOVE
META_MAPS = ["mtsamples-type-70-sample-1000", "mtsamples-type-70-sample-1001", "mtsamples-type-70-sample-108", "mtsamples-type-70-sample-109", "mtsamples-type-70-sample-110", "mtsamples-type-70-sample-111", "mtsamples-type-70-sample-112", "mtsamples-type-70-sample-114", "mtsamples-type-70-sample-1269", "mtsamples-type-70-sample-1275", "mtsamples-type-70-sample-1364", "mtsamples-type-70-sample-1365", "mtsamples-type-70-sample-1446", "mtsamples-type-70-sample-153", "mtsamples-type-70-sample-154", "mtsamples-type-70-sample-1650", "mtsamples-type-70-sample-1659", "mtsamples-type-70-sample-166", "mtsamples-type-70-sample-168", "mtsamples-type-70-sample-169", "mtsamples-type-70-sample-170", "mtsamples-type-70-sample-188", "mtsamples-type-70-sample-269", "mtsamples-type-70-sample-274", "mtsamples-type-70-sample-2773", "mtsamples-type-70-sample-471", "mtsamples-type-70-sample-970"]
def FILTER(x):
    return os.path.basename(x).split(".")[0] in META_MAPS

def failproof(func, default=None, verbose:bool=False):
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if verbose:
                print(e)
            return default
    return wrap

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

    args = parser.parse_args()

    # Read directory for all json files
    pull = FilePull(args.inpath)
    files = pull.pull(filter_statement=lambda x: x[-3:].lower() == "xmi" and FILTER(x))

    # Prepare outfile
    outfile = open(os.path.join(args.outpath, OUTFILE_NAME), "w")
    fields = ['file', '{http://www.omg.org/XMI}id', 'codingScheme', 'code', 'score', 'disambiguated', 'cui', 'tui', 'preferredText']
    csvfile = csv.DictWriter(outfile, quoting=csv.QUOTE_NONNUMERIC, fieldnames=fields)
    csvfile.writeheader()

    # Loop over directory
    for path in tqdm(files, desc="Parsing docs", unit=" doc"):

        doc = Document(path)
        records = to_records(doc.concepts)

        for item in records:
            item["file"] = os.path.basename(path)
            csvfile.writerow(item)

    outfile.close()
