#!/usr/bin/env python

"""
File: mtsample_srl_parser.py
Author: xc383@drexel.edu
Date: 2023-10-1
Purpose: A script to read a directory full of mtsamples JSONs and write them into verb JSONs using the semantic role labeler from AllenNLP.
"""

import os
import argparse
import json
from tqdm import tqdm

import sys
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)
from src.semanticrolelabel import SemanticRoleLabel

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Parses mtsamples JSON files into verb files. These files contain subject, predicate, object triplets."
    )

    parser.add_argument(
        "inpath",
        help="The path to read in the mtsample JSON. Expects files to be named 'mtsamples-type-$TYPE-sample-$SAMPLE_NUMBER.json'",
        type=str
    )

    parser.add_argument(
        "outpath",
        help="Optional. The path write the mtsamples verb JSON files. Defaults to '%s'." % os.getcwd(),
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

    extractor = SemanticRoleLabel()

    for file_name in tqdm(os.listdir(inpath), desc="Extracting verbs", unit=" doc"):
        in_file = os.path.join(inpath, file_name)
        out_file = os.path.join(outpath, file_name)
        with open(in_file, "r") as infp, open(out_file, "w") as outfp:
            doc = json.loads(infp.read())
            try:
                outfp.write(json.dumps(
                    {
                        "type_id": doc["type_id"],
                        "sample_id": doc["sample_id"],
                        "verbs": extractor.parse(
                            doc["text"]
                        )
                    }
                ))
            except Exception as e:
                print("ERROR: Document '%s' failed with error returned: %s" % (file_name, e));
