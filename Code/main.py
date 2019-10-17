from nltk.corpus import reuters
import nltk.data
from os import listdir
from os.path import isfile, join
from nltk.util import bigrams
from nltk.tokenize import TreebankWordTokenizer
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import spacy
import nltk.data
from os import listdir
from os.path import isfile, join
from nltk.util import bigrams
from nltk.tokenize import TreebankWordTokenizer
import docx
treebank_tokenizer = TreebankWordTokenizer()
# nltk.download('punkt')
# nltk.download('stopwords')

import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt




# nlp = spacy.load('en_core_web_sm')
# stopwords = spacy.lang.en.stop_words.STOP_WORDS

class Speeches(object):

    def __init__(self):
        self.base_corpus_tokens = []
        # self.num_docs = len(reuters.fileids())
        # self.sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        self.treebank_tokenizer = TreebankWordTokenizer()

    def read_directory_files(self, directory):
        """Get documents from the directory"""
        file_texts = []
        files = [f for f in listdir(directory) if isfile(join(directory, f))]
        for f in files:
            file_text = self.getText(join(directory, f))
            # print(file_text)
            file_texts.append({"file": f, "content": file_text})
        return file_texts

    def getText(self, filename):
        """Read text from documents"""
        doc = docx.Document(filename)
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        return '\n'.join(fullText)

    def tokenizeWord(self, document):
        """Tokenize documents at word level"""
        token_list = []
        for item in document:
            text = item["content"]
            words = nltk.word_tokenize(text)
            [token_list.append(token) for token in words]
        return token_list

    def getDifferences(self, wordListBase, wordListCurr):
        return set(wordListCurr).difference(set(wordListBase))

    def getFrequency(self, wordListCurr, wordListBase):
        return nltk.FreqDist(wordListCurr), nltk.FreqDist(wordListBase)

    @staticmethod
    def remove_words(word_list):
        """Remove unnecessary words such as (The, we, he,...)"""
        stopwords = nltk.corpus.stopwords.words('english')
        filtered_list = []
        [filtered_list.append(token) for token in word_list if token.lower() not in stopwords and token.isalpha()]
        return filtered_list

    def plot(self, frq_doc_base, frq_doc_curr):
        """plot frequencies"""
        doc_curr = self.remove_words(frq_doc_curr)
        doc_base = self.remove_words(frq_doc_base)
        frq_doc_curr, frq_doc_base = self.getFrequency(doc_curr, doc_base)
        frq_doc_curr.plot(20), frq_doc_base.plot(20)
        print('Most Common: ' + str(frq_doc_curr.most_common(20)))
        # plt.show()
        return doc_curr, frq_doc_base, frq_doc_curr

    def mle_distribution(self, doc_curr, frq_base, frq_curr):
        high_probability_curr = []
        mle_curr= nltk.MLEProbDist(frq_curr)
        mle_base = nltk.MLEProbDist(frq_base)

        print("MLE_jargon: "+str(mle_curr.prob('CEO, buildings')))

        for token in doc_curr:
            curr_prob = mle_curr.prob(token)
            base_prob = mle_base.prob(token)
            if curr_prob > base_prob:
                high_probability_curr.append(token)
        return high_probability_curr

    def bigrams(self, doc_base, doc_curr):
        doc_curr = self.remove_words(doc_curr) #maybe put the remove method outside because it is being called twice
        bigrams_doc = nltk.bigrams(doc_curr)
        freq_bi_doc_curr = nltk.FreqDist(bigrams_doc)
        print("Bigram current doc")
        print(freq_bi_doc_curr.most_common(20))
        freq_bi_doc_curr.plot(20)

        print("Bigram Base doc")
        doc_base = self.remove_words(doc_base)
        bigrams_base = nltk.bigrams(doc_base)
        freq_bi_base = nltk.FreqDist(bigrams_base)
        print(freq_bi_base.most_common(20))
        freq_bi_base.plot(20)

        return doc_curr, freq_bi_doc_curr, freq_bi_base, bigrams_doc, bigrams_base

    def mle_bigram(self, freq_bi_curr, freq_bi_base, bigrams_doc, word_length):
        high_probabilty_bigram = []
        Smoothed_dist_curr = nltk.LaplaceProbDist(freq_bi_curr)
        Smoothed_dist_base = nltk.LaplaceProbDist(freq_bi_base)
        print(Smoothed_dist_curr.prob(('DoD', 'Test')))
        print(Smoothed_dist_curr.logprob(('Chair', 'Force')))
        print(Smoothed_dist_curr.generate())

        slogprob = 0
        for bigram_words in bigrams_doc:
            logprob_curr = Smoothed_dist_curr.logprob(bigram_words)
            slogprob += logprob_curr
            logprob_base = Smoothed_dist_base.logprob(bigram_words)
            if logprob_curr > logprob_base:
                high_probabilty_bigram.append(bigram_words)

        return high_probabilty_bigram #slogprob / word_length



dir_base = 'C:/Users/Giraldo/Documents/NLC/NLP/Data/Base Data'
dir_curr = 'C:/Users/Giraldo/Documents/NLC/NLP/Data/Current Data'
speech = Speeches()

base_speeches = speech.read_directory_files(dir_base)
curr_speeches = speech.read_directory_files(dir_curr)
tokenWord_base = speech.tokenizeWord(base_speeches)
tokenWord_curr = speech.tokenizeWord(curr_speeches)

differences = speech.getDifferences(tokenWord_base, tokenWord_curr)
doc_curr, frq_doc_base, frq_doc_curr = speech.plot(tokenWord_base, tokenWord_curr)
mle_probab = speech.mle_distribution(doc_curr, frq_doc_base, frq_doc_curr )

doc_curr, freq_bi_curr, freq_bi_base, bigrams_doc, bigrams_base = speech.bigrams(tokenWord_base, tokenWord_curr)
high_prob_bigram= speech.mle_bigram(freq_bi_curr,freq_bi_base,bigrams_doc, len(tokenWord_curr))


#/ print('\n'.join('{}: {}'.format(*k) for k in enumerate(differences)))
print("length base: "+str(len(tokenWord_base)))
print("length curr: "+str(len(tokenWord_curr)))
print("length differences: " +str(len(differences)))
print("High probability: "+str((mle_probab)))
print("High probability Bigrams: "+str(high_prob_bigram))
# print("bigram curr: ")
# print('\n'.join('{}: {}'.format(*k) for k in enumerate(bigrams_doc)))
# print("bigram base: ")
# print('\n'.join('{}: {}'.format(*k) for k in enumerate(bigrams_base)))

# import pandas as pd
# words_df = pd.DataFrame({'word': list(frq_doc_curr.keys()), 'count': list(frq_doc_curr.values())})
#
#
# import plotly.express as px
# tips = px.data.tips()
# fig = px.bar(words_df, x="word", y="count")
# fig.show()




