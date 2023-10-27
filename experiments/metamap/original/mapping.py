#!/usr/bin/env python
"""
File: mapping.py
Author: xc383@drexel.edu
Date: 2023-10-18
Purpose: A mapping class and associated utilities for Metamap output.
"""

# TODO: Add PIs to datamodel

from typing import List, Optional
from dataclasses import dataclass, asdict, astuple
import json

from typing import List, Optional
from dataclasses import dataclass, asdict, astuple

@dataclass
class Mapping:

    cui: str
    start_pos: int
    length: int
    semantic_types: List[str]

    source: str
    score: int
    matched: str
    preferred: str
    matched_words: List[str]

    is_head: Optional[bool]=None
    negated: Optional[bool]=None

    def __str__(self) -> str:
        json.dumps(self.asdict)

    def asdict(self) -> dict:
        return asdict(self)

    def astuple(self) -> dict:
        return astuple(self)

def map_to_uterance(mapping: dict) -> Mapping:
    maps = []
    for position in mapping["ConceptPIs"]:
        maps.append(Mapping(
            cui=mapping.get("CandidateCUI"),
            start_pos=int(position.get("StartPos")),
            length=int(position.get("Length")),
            semantic_types=mapping.get("SemTypes"),
            source=mapping.get("Sources")[0],
            score=int(mapping.get("CandidateScore")),
            matched=mapping.get("CandidateMatched"),
            matched_words=mapping.get("MatchedWords"),
            preferred=mapping.get("CandidatePreferred"),
            is_head=True if mapping.get("IsHead") == "no" else False,
            negated=True if mapping.get("Negated") == "no" else False
        )
    )

    return maps