#!/usr/bin/env python
"""
File: metamap_parser.py
Author: xc383@drexel.edu
Date: 2023-10-27
Purpose: A parser for metamap JSONs.
"""

import re

def breakdown_criteria_text(text: str) -> dict[str, str]:
    """
    Breakdown a criteria specification text into sections. Will parse into list of inclusion sections and exclusion sections.
    :param text (str): A text to parse.
    :returns: A dict of inclusion sections list and exclusion sections list.
    """
    criteria_split_pattern = r"(\w+)\s+[Cc]riteria\W?"
    split_pattern = re.compile(criteria_split_pattern)

    doc = {
        "inclusion": [],
        "exclusion": []
    }

    criteria_parts = re.split(split_pattern, text)
    i = 0

    while i < len(criteria_parts):
        lower_case_part = criteria_parts[i].lower()
        if lower_case_part == "inclusion":
            i += 1
            doc[lower_case_part].append(criteria_parts[i])
        elif lower_case_part == "exclusion":
            i += 1
            doc[lower_case_part].append(criteria_parts[i])
        i += 1

    return doc

def tolines(text: str) -> list[str]:
    """
    Break appart all newlines. Will conflat multiple newlines together in splitting.
    :param text (str): A text to split.
    :returns: A list of strings.
    """
    newlines_break = re.compile(r"\n+")
    return re.split(newlines_break, text)

def check_valid(text: str) -> bool:
    """
    Check if a text is valid.
    :param text (str): A text to check.
    :returns: A boolean true if valid and false otherwise.
    """
    return True

def process_criteria(text: str, min_length: int=10) ->list[tuple]:
    """
    Process a critera into tuples. Each resulting tuple contains the (criteria type, section index, criteria text).
    :param text (str): A text to parse.
    :param min_length (int): Optional, the single criteria length threshold. All criteria with less than this many charecters is removed. Defaults to 10.
    :returns: A list of tuples.
    """
    criteria = []
    sections = breakdown_criteria_text(text)

    inclusion = "\n".join(sections["inclusion"])
    exclusion = "\n".join(sections["exclusion"])

    if check_valid(inclusion):
        cnt = 0
        for item in filter(lambda x: len(x) > 9, tolines(inclusion)):
            criteria.append(("inclusion", cnt, item))
            cnt += 1

    if check_valid(exclusion):
        cnt = 0
        for item in filter(lambda x: len(x) > 9, tolines(exclusion)):
            criteria.append(("exclusion", cnt, item))
            cnt += 1

    return criteria
