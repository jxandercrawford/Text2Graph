#!/usr/bin/env python

"""
File: xml_tools.py
Author: xc383@drexel.edu
Date: 2023-10-16
Purpose: A set of functions for parsing XML.
"""

from lxml.etree import Element
from typing import List

def to_records(nodes: List[Element]) -> List[dict[str, str]]:
    """
    Convert a list of tree nodes to a list of dictionaries.
    :param nodes (list): Takes a list of tree nodes from an XML parsing.
    :returns: A list of dictionaries.
    """
    data = []
    for node in nodes:
        data.append({k:v for k, v in node.items()})
    return data
