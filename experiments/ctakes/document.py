import os
from lxml import etree
import json
import sys

# Load ctakes directory to path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)

with open(os.path.join(ROOT_DIR, "schema", "ctakes_output_schema.json"), "r") as file:
    CLINICAL_PIPELINE_DICT = json.load(file)

class Document:
    """
    A cTakes XMI file wrapper.
    :param path (str): A path to a xTakes XMI file.
    :param mapping (dict): Optional, a mapping of the XMI schema. Defaults to ctakes_output_schema.json.
    """

    def __init__(self, path:str, mapping:dict=CLINICAL_PIPELINE_DICT):
        self.__path = path
        self.__validate_path()

        # Create xml parser
        self.__tree = etree.parse(path)
        self.__namespaces = self.__tree.getroot().nsmap.copy()
        self.__root = root = self.__tree.getroot()

    def __str__(self):
        return self.get_xpath(CLINICAL_PIPELINE_DICT["text"]["xpath"])[0].get("sofaString")

    def __validate_path(self):
        return os.path.isfile(self.__path)

    @property
    def path(self):
        return self.__path

    @property
    def root(self):
        return self.__root

    def get_xpath(self, xpath:str):
        return self.__root.xpath(xpath, namespaces=self.__namespaces)

    def get_id(self, id: int):
        elems = root.xpath(".//*[@xmi:id='%d']" % x, namespaces=namespaces)
        if elems:
            return elems[0]
        return None

    @property
    def sentences(self):
        return self.get_xpath(CLINICAL_PIPELINE_DICT["index"]["syntax"]["sentence"]["xpath"])

    @property
    def newlines(self):
        return self.get_xpath(CLINICAL_PIPELINE_DICT["index"]["syntax"]["newline"]["xpath"])

    @property
    def words(self):
        return self.get_xpath(CLINICAL_PIPELINE_DICT["index"]["syntax"]["word"]["xpath"])

    @property
    def punctuations(self):
        return self.get_xpath(CLINICAL_PIPELINE_DICT["index"]["syntax"]["punctuation"]["xpath"])

    @property
    def numbers(self):
        return self.get_xpath(CLINICAL_PIPELINE_DICT["index"]["syntax"]["number"]["xpath"])

    @property
    def symbols(self):
        return self.get_xpath(CLINICAL_PIPELINE_DICT["index"]["syntax"]["symbol"]["xpath"])

    @property
    def chunks(self):
        return self.get_xpath(CLINICAL_PIPELINE_DICT["index"]["syntax"]["chunk"]["xpath"])

    @property
    def dependants(self):
        return self.get_xpath(CLINICAL_PIPELINE_DICT["index"]["syntax"]["dependant"]["xpath"])

    @property
    def predicates(self):
        return self.get_xpath(CLINICAL_PIPELINE_DICT["index"]["syntax"]["predicate"]["xpath"])

    @property
    def numerals(self):
        return self.get_xpath(CLINICAL_PIPELINE_DICT["index"]["mention"]["numeral"]["xpath"])

    @property
    def measurements(self):
            return self.get_xpath(CLINICAL_PIPELINE_DICT["index"]["mention"]["measurement"]["xpath"])

    @property
    def fractions(self):
        return self.get_xpath(CLINICAL_PIPELINE_DICT["index"]["mention"]["fraction"]["xpath"])

    @property
    def medications(self):
        return self.get_xpath(CLINICAL_PIPELINE_DICT["index"]["mention"]["medication"]["xpath"])

    @property
    def diseases(self):
        return self.get_xpath(CLINICAL_PIPELINE_DICT["index"]["mention"]["disease"]["xpath"])

    @property
    def symptoms(self):
        return self.get_xpath(CLINICAL_PIPELINE_DICT["index"]["mention"]["symptom"]["xpath"])

    @property
    def procedures(self):
        return self.get_xpath(CLINICAL_PIPELINE_DICT["index"]["mention"]["procedure"]["xpath"])

    @property
    def anatomys(self):
        return self.get_xpath(CLINICAL_PIPELINE_DICT["index"]["mention"]["anatomy"]["xpath"])

    @property
    def semantic_argument(self):
        return self.get_xpath(CLINICAL_PIPELINE_DICT["index"]["semantic_role"]["argument"]["xpath"])

    @property
    def semantic_relation(self):
        return self.get_xpath(CLINICAL_PIPELINE_DICT["index"]["semantic_role"]["relation"]["xpath"])

    @property
    def concepts(self):
        return self.get_xpath(CLINICAL_PIPELINE_DICT["concept"]["umls"]["xpath"])
