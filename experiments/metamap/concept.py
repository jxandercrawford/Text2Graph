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
class Concept:

    # Metadata
    document_id: int
    utterance_id: int
    phrase_id: int
    mapping_id: int
    canidate_id: int

    cui: str
    start_pos: int
    end_pos: int
    document_offset: int
    semantic_types: List[str]

    sources: List[str]
    score: int
    matched: str
    preferred: str
    is_head: bool
    negated: bool

    file_name: Optional[str]

    def __str__(self) -> str:
        json.dumps(self.asdict)

    def asdict(self) -> dict:
        return asdict(self)

    def astuple(self) -> dict:
        return astuple(self)

def dict_to_concept(d: dict, file_name: str=None) -> Concept:
    return Concept(
            document_id=d.get("document_n"),
            utterance_id=d.get("utterance_n"),
            phrase_id=d.get("phrase_n"),
            mapping_id=d.get("mapping_n"),
            canidate_id=d.get("canidate_n"),
            cui=d.get("CandidateCUI"),
            start_pos=d.get("StartPos"),
            end_pos=d.get("EndPos"),
            document_offset=d.get("document_start"),
            semantic_types=d.get("SemTypes"),
            sources=d.get("Sources"),
            score=int(d.get("CandidateScore")),
            matched=d.get("CandidateMatched"),
            preferred=d.get("CandidatePreferred"),
            is_head=d.get("IsHead"),
            negated=d.get("Negated"),
            file_name=file_name,
        )