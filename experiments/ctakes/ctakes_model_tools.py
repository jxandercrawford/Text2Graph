#!/usr/bin/env python
"""
File: ctakes_model_tools.py
Author: xc383@drexel.edu
Date: 2023-10-30
Purpose: Tools for working with ctakes_model.
"""

import os
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))     # For modules within this experiment
ROOT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))     # For modules within this project
sys.path.append(BASE_DIR)
sys.path.append(ROOT_DIR)

import pandas as pd
from ctakes_model import Concept, Mention
from document import Document
from xml_tools import to_records

def dict_to_mention(d: dict, mention_class: Mention=Mention) -> Mention:
    """
    Given a dictionary return a Mention constructed out of keys found in cTakes XMI output.
    :param d (dict): A dictionary to parse.
    :param mention_class (Mention): Use a subclass of mention.
    :returns: A mention.
    """
    c = dict_to_concept(d)
    m = mention_class(
        start=int(d.get("begin")),
        end=int(d.get("end")),
        subject=d.get("subject"),
        concept=c,
        polarity=int(d.get("polarity")),
        uncertainty=int(d.get("uncertainty")),
        confidence=float(d.get("confidence")),
        conditional=d.get("conditional") == "true",
        generic=d.get("generic") == "true",
        history=int(d.get("historyOf"))
    )

    return m

def dict_to_concept(d: dict) -> Concept:
    """
    Given a dictionary return a Concept constructed out of keys found in cTakes XMI output.
    :param d (dict): A dictionary to parse.
    :returns: A concept.
    """
    return Concept(
        scheme=d.get("codingScheme").lower(),
        cui=d.get("cui"), tui=d.get("tui"),
        text=d.get("preferredText"),
        score=float(d.get("score")),
        disambiguated=d.get("disambiguated") == "true"
    )

import re

def get_mentions(doc: Document):
    """
    Pull all mentions from a cTakes Document.
    :param doc (Document): A cTakes document to parse mentions from.
    :returns: A list of dicts containing each mention.
    """

    def prep(items, name: str):
        """
        Helper function.
        """
        new_items = []

        mentions = to_records(items)
        for mention in mentions:
            for concept in map(int, re.split(r"\s+", mention.pop("ontologyConceptArr"))):
                new_mention = mention
                new_mention["ontologyConceptID"] = concept
                new_items.append(new_mention)
            new_mention["type"] = name
        return new_items

    records = []

    # records += prep(doc.numerals, "numeral")
    # records += prep(doc.measurements, "measurement")
    # records += prep(doc.fractions, "fraction")
    records += prep(doc.medications, "medication")
    records += prep(doc.diseases, "disease")
    records += prep(doc.symptoms, "symptom")
    records += prep(doc.procedures, "procedure")
    records += prep(doc.anatomys, "anatomy")

    concepts = pd.DataFrame.from_records(to_records(doc.concepts))
    concepts["{http://www.omg.org/XMI}id"] = concepts["{http://www.omg.org/XMI}id"].apply(int)

    return pd.merge(
        pd.DataFrame.from_records(records),
        concepts,
        left_on="ontologyConceptID",
        right_on="{http://www.omg.org/XMI}id"
    ).to_dict(orient="records")
