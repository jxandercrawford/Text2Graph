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
    Breakdown a criteria specification text into sections. Will parse into list of criteria sections.
    :param text (str): A text to parse.
    :returns: A dict of sections.
    """
    criteria = re.findall(r"\n?(.*clusion)\s+[Cc]riteria\S?\n", text)
    if not criteria:
        return {}
    blocks = re.split("(?:" + "|".join(criteria) + ")\\s+[Cc]riteria\\S?", text)
    sections = {str(k).lower().replace(" ", "_"): v for k, v in zip(criteria, list(filter(lambda x: x != "", blocks)))}

    for k, v in sections.items():
        sections[k] = tolines(v)

    return sections

def tolines(text: str) -> list[str]:
    """
    Break appart all newlines. Will conflat multiple newlines together in splitting.
    :param text (str): A text to split.
    :returns: A list of strings.
    """
    if text is None:
        return None
    newlines_break = re.compile(r"\n+")
    return re.split(newlines_break, text)

def check_valid(text: str) -> bool:
    """
    Check if a text is valid.
    :param text (str): A text to check.
    :returns: A boolean true if valid and false otherwise.
    """
    return True

def filter_criteria(text: str) -> bool:
    return text != ""

def process_criteria(text: str, min_length: int=10) ->list[tuple]:
    """
    Process a critera into tuples. Each resulting tuple contains the (criteria type, section index, criteria text).
    :param text (str): A text to parse.
    :param min_length (int): Optional, the single criteria length threshold. All criteria with less than this many charecters is removed. Defaults to 10.
    :returns: A list of tuples.
    """
    criteria = []
    sections = breakdown_criteria_text(text)

    for key in sections.keys():
        cnt = 0
        values = sections.get(key)
        if values is None:
            continue
        for val in values:
            if filter_criteria(val):
                criteria.append([key, cnt, val])
                cnt += 1

    return criteria
