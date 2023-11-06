import argparse
import os
import sys
import csv
from io import StringIO
BASE_DIR = os.path.dirname(os.path.abspath(__file__))     # For modules within this experiment
ROOT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))     # For modules within this project
sys.path.append(BASE_DIR)
sys.path.append(ROOT_DIR)

from criteria import process_criteria

MIN_CRITERIA_LENGTH = 10

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Parses a critera text into a comma delimiated set of fields."
    )

    parser.add_argument(
        "-l", "--min_length",
        help="Optional, the single criteria length threshold. All criteria with less than this many charecters is removed. Defaults to %d." % MIN_CRITERIA_LENGTH,
        type=int,
        default=MIN_CRITERIA_LENGTH
    )

    parser.add_argument("stdin", nargs="?", type=argparse.FileType("r"), default=sys.stdin)

    args = parser.parse_args()
    out = StringIO()
    fd = csv.writer(out, quoting=csv.QUOTE_NONNUMERIC)

    criteria = process_criteria("".join(args.stdin), MIN_CRITERIA_LENGTH)
    fd.writerows(criteria)
    print(out.getvalue())