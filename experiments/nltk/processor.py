
import nltk
from nltk import word_tokenize
from nltk.tokenize import sent_tokenize, word_tokenize

class Document():

    def __init__(self, doc: str):
        self.__doc = doc
        self.__sentences = None
        self.__tokenized_sentences = None
        self.__part_of_speach = None

        self.__sent_tokenize()
        self.__word_tokenize()
        self.__pos()

    def __str__(self):
        return self.__doc

    def __sent_tokenize(self):
        self.__sentences = sent_tokenize(self.__doc)
    
    def __word_tokenize(self):
        self.__tokenized_sentences = []
        for sentence in self.__sentences:
            self.__tokenized_sentences.append(word_tokenize(sentence))

    def __pos(self):
        self.__part_of_speach = []
        for sentence in self.__tokenized_sentences:
            self.__part_of_speach.append(nltk.pos_tag(sentence))
    
    @property
    def tokens(self):
        return self.__tokenized_sentences

    @property
    def pos(self):
        return self.__part_of_speach