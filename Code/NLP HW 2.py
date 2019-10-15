from nltk.corpus import reuters
import nltk.data
from os import listdir
from os.path import isfile, join
from nltk.util import bigrams
from nltk.tokenize import TreebankWordTokenizer
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import spacy

nlp = spacy.load('en_core_web_sm')
stopwords = spacy.lang.en.stop_words.STOP_WORDS


class jargon(object):
    def __init__(self):
        self.base_corpus_tokens = []
        self.num_docs = len(reuters.fileids())
        self.sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        self.treebank_tokenizer = TreebankWordTokenizer()


    def reuters(self):
        #  this has a large number of files...
        # you might wish to limit the number of documents you use while developing your technique
        # ex. reuters.fileids()[0:25]
        reuters_doc=[]
        for doc in reuters.fileids():
            # doc_text = reuters.open(doc).read()
            doc_text = list(reuters.words(doc))
            # this doc_text variable will give you a text version of the news article. This could be tokenized.
            for words in doc_text:
                reuters_doc.append(words)
        print(len(reuters_doc))
        return reuters_doc

    def read_file(self, filename):
        input_file_text = open(filename, encoding='utf-8').read()
        return input_file_text

    def read_directory_files(self, directory):
        file_texts = []
        files = [f for f in listdir(directory) if isfile(join(directory, f))]
        for f in files:
            file_text = self.read_file(join(directory, f))
            file_texts.append({"file": f, "content": file_text })
        print(len(file_texts))
        return file_texts

    @staticmethod
    def tokenize_word(document):

        token_list = []
        for item in document:
            text = item["content"]
            doc = nlp(text)
            """tokenize, remove stop words and punctuation"""
            [token_list.append(token.text) for token in doc if token.is_stop is False and token.is_punct is False]#!= True]

        print(len(token_list))
        return token_list


    def del_stop_words(self):
        stop_words = stopwords.words('english')
        pass

    def differences(self):
        pass

    def frequency(self):
        pass

    def distribution(self):
        pass


dir_base = "C:/Users/Cristina/Documents/GWU/NLP/HW/HW2/data"
jargon = jargon()
reuters = jargon.reuters()
file_texts = jargon.read_directory_files(dir_base)
file_texts = jargon.tokenize_word(file_texts)

