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
from database import Database

MIN_CRITERIA_LENGTH = 10
SELECT_STATEMENT = "SELECT nct_id, criteria FROM eligibilities;"
BASE_CREDENTIALS = {
    "host": "",
    "database": "aact",
    "user": "xc383@drexel.edu",
    "password": ""
}

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

    args = parser.parse_args()
    out = StringIO()
    fd = csv.writer(out, quoting=csv.QUOTE_NONNUMERIC)
    db = Database(**BASE_CREDENTIALS)

    texts = db.execute_yield(SELECT_STATEMENT)

    for item in texts:
        nct_id, text = item.values()

        try:
            criteria = process_criteria("".join(text), MIN_CRITERIA_LENGTH)
            fd.writerows(map(lambda x: [nct_id, *x], criteria))
            print(out.getvalue(), file=sys.stdout)
        except Exception as e:
            print("ERROR: Issue parsing '%s' resulting in: %s" % (nct_id, e), file=sys.stderr)
