#!/usr/bin/env python
"""
File: mapping.py
Author: xc383@drexel.edu
Date: 2023-10-18
Purpose: A mapping class and associated utilities for Metamap output.
"""

from typing import List, Optional
from dataclasses import dataclass, asdict, astuple
import json

@dataclass
class Mapping:

    cui: str
    source: str
    score: int
    matched: str
    preferred: str
    matched_words: List[str]
    semantic_types: List[str]

    is_head: Optional[bool]=None
    negated: Optional[bool]=None

    def __str__(self) -> str:
        json.dumps(self.asdict)

    def asdict(self) -> dict:
        return asdict(self)

    def astuple(self) -> dict:
        return astuple(self)

def map_to_uterance(mapping: dict) -> Mapping:
    """
    Parse a dictionary mapping from Metamap output JSON into a Mapping object.
    :param mapping (dict): The mapping objects found by path `AllDocuments`>`Document`>`Utterances`>`Phrases`>`Mappings`>`MappingCandidates`.
    :returns: A Mapping object.
    """
    ret = Mapping(
        cui=mapping.get("CandidateCUI"),
        source=mapping.get("Sources")[0],
        score=int(mapping.get("CandidateScore")),
        matched=mapping.get("CandidateMatched"),
        matched_words=mapping.get("MatchedWords"),
        preferred=mapping.get("CandidatePreferred"),
        semantic_types=mapping.get("SemTypes"),
        is_head=mapping.get("isHead")
    )

    if mapping.get("IsHead") == "no":
        ret.is_head = False
    elif mapping.get("IsHead") == "yes":
        ret.is_head = True

    if mapping.get("Negated") != "0":
        ret.negated = True
    else:
        ret.negated = False

    return ret
