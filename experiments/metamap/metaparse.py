
import re
from flatten_json import flatten
import pandas as pd


def remove_multinewline(text: str) -> str:
    """
    Will remove all instances of multiple consecutive newlines and replace with a single newline.

    Example: 'Hello\\n\\nWorld!' => 'Hello\\nWorld!'

    :param text (str): Text to remove multiple newlines.
    :returns: The same text with only single newlines.
    """
    return "\n".join(re.split(re.compile(r"\n+"), text))


def calc_relative_positions(data: dict) -> dict[int, int]:
    """
    Given a Metamap output JSON object calculate the positions of each document based relative to the start of the document.

    NOTE: Each document is cut by newline(s). These positions do not reflect this. To remediate use function `remove_multinewline()`.
    :param data (dict): Metamap JSON object.
    :returns: A dict containing relative positons for each document.
    """

    # Flatten dict
    flat_data = flatten(data)

    # Extract document keys
    doc_patterns = {
    "start": "AllDocuments_(\\d+)_Document_Utterances_(\\d+)_UttStartPos",
    "length": "AllDocuments_(\\d+)_Document_Utterances_(\\d+)_UttLength"
    }
    doc_keys = re.findall("AllDocuments_(\\d+)_Document_Utterances_(\\d+)", " ".join(flat_data.keys()))

    positions = []
    # For each unique index pull positioning
    for doc, utt in set(doc_keys):
        d = {}
        d["document_n"] = int(doc)
        d["utterance_n"] = int(utt)
        d["utterance_start"] = flat_data.get("AllDocuments_%s_Document_Utterances_%s_UttStartPos" % (doc, utt))
        d["utternace_length"] = flat_data.get("AllDocuments_%s_Document_Utterances_%s_UttLength" % (doc, utt))
        positions.append(d)

    df = pd.DataFrame.from_records(positions)

    # Ensure positions in order and integers
    df = df.sort_values(["document_n", "utterance_n"])
    df["utterance_start"] = df.utterance_start.apply(int)
    df["utternace_length"] = df.utternace_length.apply(int)

    # Create relative positioning
    df["utterance_relative_start"] = df.utternace_length.cumsum() - df.utternace_length

    return df.groupby("document_n").utterance_relative_start.min().rename("document_start").reset_index().to_dict(orient="records")


def pull_concepts(data: dict) -> list[dict]:
    """
    Pulls concepts from a Metamap JSON.
    :param data (dict): Metamap JSON object.
    :returns: A dict containing concepts broken down into words.
    """

    # Flatten metamap JSON
    flat_data = flatten(data)

    # Patterns to fetch
    index_pattern = "AllDocuments_(\\d+)_Document_Utterances_(\\d+)_Phrases_(\\d+)_Mappings_(\\d+)_MappingCandidates_(\\d+)_ConceptPIs_(\\d+)"
    metamap_patterns = {
        "concepts": {
            "pattern": "AllDocuments_(\\d+)_Document_Utterances_(\\d+)_Phrases_(\\d+)_Mappings_(\\d+)_MappingCandidates_(\\d+)_",
            "fields": [
                "CandidateCUI",
                "SemTypes",
                "Sources",
                "CandidateScore",
                "CandidateMatched",
                "CandidatePreferred",
                "IsHead",
                "Negated"
            ]
        },
        "canidates": {
            "pattern": "AllDocuments_(\\d+)_Document_Utterances_(\\d+)_Phrases_(\\d+)_Mappings_(\\d+)_MappingCandidates_(\\d+)_ConceptPIs_(\\d+)_",
            "fields": [
                "StartPos",
                "Length"
            ]
        },
        "words": {
            "pattern": "AllDocuments_(\\d+)_Document_Utterances_(\\d+)_Phrases_(\\d+)_Mappings_(\\d+)_MappingCandidates_(\\d+)_MatchedWords_(\\d+)",
            "fields": [""]
        }
    }

    # Create patterns
    patterns = []
    for key in metamap_patterns.keys():
        for field in metamap_patterns[key]["fields"]:
            patterns.append(metamap_patterns[key]["pattern"] + field)
    string_patterns = [(pattern.count("(\\d+)"), pattern.replace("(\\d+)", "%s")) for pattern in patterns]

    # Pull indexes to use with patterns
    df = pd.DataFrame(re.findall(index_pattern, " ".join(flat_data.keys())), columns=["document_n", "utterance_n", "phrase_n", "mapping_n", "canidate_n", "word_n"])
    df = df.drop_duplicates()
    all_indexes = df.values.tolist()

    # Create unique index for each pattern
    df["idx"] = df.apply(lambda x: "".join(map(str, x)), axis=1).apply(int)

    items = []
    list_patterns = ["SemTypes", "Sources"]

    # Parse JSON
    for index in all_indexes:
        d = {}
        d["document_n"] = int(index[0])
        d["utterance_n"] = int(index[1])
        d["phrase_n"] = int(index[2])
        d["mapping_n"] = int(index[3])
        d["canidate_n"] = int(index[4])
        d["word_n"] = int(index[5])

        for n, pattern in string_patterns:
            field_name = pattern.split("_")[-1]
            indexed_pattern = pattern % tuple(index[:n])

            if field_name == "%s":
                field_name = "MatchedWord"

            if field_name in list_patterns:
                list_item_pattern = "_".join(indexed_pattern.split("_")[:-1]) + "_" + field_name + "_%s"
                i = 0
                d[field_name] = []
                while 1:
                    if flat_data.get(list_item_pattern % i) is not None:
                        d[field_name].append(flat_data.get(list_item_pattern % i))
                        i += 1
                    else:
                        break
            elif field_name == "MatchedWord":
                d[field_name] = flat_data.get(indexed_pattern)
            else:
                d[field_name] = flat_data.get(indexed_pattern)

        # Format correctly
        d["CandidateScore"] = int(d["CandidateScore"])
        d["Negated"] = d.get("Negated") == "1"
        d["Negated"] = d.get("IsHead") == "yes"
        d["StartPos"] = int(d["StartPos"])
        d["Length"] = int(d["Length"])

        items.append(d)

    return items


def conflate_instances(data: dict) -> list[dict]:
    """
    Conflate the output of pull_concepts() by merging all the words of each concept together.
    :param data (dict): The pulled concepts dict.
    :returns: A list of dicts of conflated words into single concept instances.
    """
    df = pd.DataFrame(data)
    canidate_groups = df.groupby(["document_n", "utterance_n", "phrase_n", "mapping_n", "canidate_n"])
    canidate_end = (canidate_groups.max("StartPos").StartPos + canidate_groups.max("StartPos").Length).rename("EndPos")
    canidate_start = canidate_groups.StartPos.min()
    canidates = canidate_start.to_frame().join(canidate_end.to_frame()).reset_index()

    canidate_cols = ['document_n', 'utterance_n', 'phrase_n', 'mapping_n', 'canidate_n', 'CandidateCUI', 'SemTypes', 'Sources', 'CandidateScore', 'CandidateMatched', 'CandidatePreferred', 'IsHead', 'Negated']
    dx = pd.merge(df.loc[:, canidate_cols], canidates, on=["document_n", "utterance_n", "phrase_n", "mapping_n", "canidate_n"])
    return dx.drop_duplicates(["document_n", "utterance_n", "phrase_n", "mapping_n", "canidate_n"]).to_dict(orient="records")


def process_metamap_json(data: dict) -> list[dict]:
    """
    Will process a given metamap json.
    :param data (dict): Metamap JSON object.
    :returns: A list containing concepts in dict format.
    """
    positions = pd.DataFrame.from_records(calc_relative_positions(data))
    concept_words = pd.DataFrame.from_records(pull_concepts(data))
    concepts = pd.DataFrame.from_records(conflate_instances(concept_words))
    return pd.merge(concepts, positions, on=["document_n"]).to_dict(orient="records")