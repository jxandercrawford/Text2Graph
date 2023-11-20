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
SELECT_STATEMENT = "SELECT setseed(.5); SELECT e.nct_id, EXTRACT( YEAR FROM s.start_date ) AS start_year, e.criteria FROM eligibilities e JOIN studies s ON e.nct_id = s.nct_id WHERE EXTRACT( YEAR FROM s.start_date ) > 2020 ORDER BY RANDOM() LIMIT 385;"
# SELECT_STATEMENT = """
# SELECT setseed(.5);
# WITH crits AS (
# 	SELECT
# 		e.nct_id,
# 		e.criteria,
# 		EXTRACT(year FROM start_date) AS start_year,
# 		row_number() OVER (PARTITION BY EXTRACT(year FROM start_date) ORDER BY random()) AS rid
# 	FROM eligibilities e
# 	JOIN studies s
# 	ON e.nct_id = s.nct_id
# ) SELECT nct_id, criteria, start_year FROM crits WHERE rid <= 10;
# """

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
        nct_id, year, text = item.values()

        if text is None:
            continue

        try:
            criteria = process_criteria(text, MIN_CRITERIA_LENGTH)
            fd.writerows(map(lambda x: [nct_id, year, *x], criteria))
            print(out.getvalue()[:-1], file=sys.stdout)
            out.flush()
        except Exception as e:
            print("ERROR: Issue parsing '%s' resulting in: %s" % (nct_id, e), file=sys.stderr)
