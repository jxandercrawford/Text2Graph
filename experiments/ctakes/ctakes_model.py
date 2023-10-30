#!/usr/bin/env python
"""
File: ctakes_model.py
Author: xc383@drexel.edu
Date: 2023-10-30
Purpose: A data model for cTakes.
"""

import os
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))     # For modules within this experiment
ROOT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))     # For modules within this project
sys.path.append(BASE_DIR)
sys.path.append(ROOT_DIR)

from abc import abstractmethod
from dataclasses import dataclass, asdict, astuple
from typing import Optional, List
from json import dumps

@dataclass
class ConversionTrait:

    def asdict(self) -> dict:
        """
        Convert class into dictionary.
        :returns: class as a dict.
        """
        return asdict(self)

    def astuple(self) -> tuple:
        """
        Convert class into a tuple.
        :returns: class as a tuple.
        """
        return astuple(self)

    def asjson(self, indentation:int=None) -> str:
        """
        Convert class into a JSON string.
        :param indentation (int): Optional, the indentation level for the JSON string. Defaults to None.
        :returns: class as a JSON string.
        """
        if indentation:
            return dumps(self.asdict(), indent=indentation)
        return dumps(self.asdict())


@dataclass
class Serializable(ConversionTrait):

    @abstractmethod
    def serialize(self) -> str:
        pass

@dataclass
class Index(ConversionTrait):
    start: int
    end: int

@dataclass
class Concept(ConversionTrait):
    scheme: str
    cui: str
    tui: str
    text: str

    score: Optional[float] = None
    disambiguated: Optional[bool] = None

@dataclass
class Mention(Index):
    subject: str
    concept: Concept

    polarity: Optional[int] = None
    uncertainty: Optional[float] = None
    confidence: Optional[float] = None
    conditional: Optional[bool] = None
    generic: Optional[bool] = None
    history: Optional[int] = None

    def asdict(self, flatten: bool=False):
        d = asdict(self)
        if flatten:
            for k, v in d.pop("concept").items():
                d["concept_" + k] = v
        return d

    def asjson(self, indentation:int=None, flatten: bool=False):
        d = asdict(self)
        if flatten:
            for k, v in d.pop("concept").items():
                d["concept_" + k] = v
        if indentation:
            return dumps(d, indent=indentation)
        return dumps(d)

@dataclass
class Medication(Mention):

    @property
    def typestr(self):
        return "medication"

@dataclass
class Disease(Mention):

    @property
    def typestr(self):
        return "disease"

@dataclass
class Symptom(Mention):

    @property
    def typestr(self):
        return "symptom"

@dataclass
class Procedure(Mention):

    @property
    def typestr(self):
        return "procedure"

@dataclass
class Anatomy(Mention):

    @property
    def typestr(self):
        return "anatomy"