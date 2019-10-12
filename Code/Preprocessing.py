import nltk
import pandas as pd
from docx import Document
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from textblob import Word
import en_core_web_sm
from spacy.lang.en import English

import os
class PreprocessingText:

    def __init__(self, pr_df):
        self.pr_df = pr_df

    # Tokenization - separates words
    def tokenization(self):
        nlp = English()
        my_doc = nlp(str(self.pr_df))
        token_list = []
        for token in my_doc:
            token_list.append(token.text)
        self.pr_df = token_list
        return self.pr_df



def main():

    # RENZO: File Upload - Begin --------------

    #Put the path of Data file here
    file_path = ('/Users/renzocastagnino/Google Drive/MASTER DATA SCIENCE/SEMESTER 2/Natural Language ''Process/Project/Data/Salt Lake City_ UT - 2016.docx')
    raw_text = Document(file_path)

    #Renzo: Creates an Document object with the paragraphs of the DOCX.
    para_text = []
    for i in raw_text.paragraphs:
        para_text.append(i.text)

    #Converts the DOC Object to a regular list.
    txt_data = []
    for word in para_text:
        txt_data.append(str(word))

    # RENZO: File Upload - End --------------


    # RENZO: Classes - Begin --------------
    pre_text = PreprocessingText(txt_data)
    text_clean = pre_text.tokenization()
    print(text_clean)
    # RENZO: Classes - End --------------

main()


# RENZO: THE CODE BELLOW IS UNDER REVIEW:

# def lematization(self):
#     self.pr_df = self.pr_df
#     self.pr_df = self.pr_df.apply(
#         lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
#     return self.pr_df
#
#
# def stemming(self):
#     st = PorterStemmer()
#     self.pr_df = self.pr_df.apply(
#         lambda x: " ".join([st.stem(word) for word in x.split()]))
#     return self.pr_df
#
#     def identify_city_state_year(self):
#         nlp = en_core_web_sm.load()
#         doc = nlp(self.pr_df)
#         return([(X.text, X.label_) for X in doc.ents])
#
#     # Remove stop words and reassign to the same column
#     def remove_stop_w(self):
#         stop_words = stopwords.words('english')
#         self.pr_df = str(self.pr_df).apply(
#             lambda x: " ".join(x for x in str(x).split() if x not in stop_words))
#
#         # Delete all the numbers
#         self.pr_df = self.pr_df.str.replace('\d+', '')
#         self.pr_df = self.pr_df.dropna().reset_index(
#             drop=True)  # Renzo: delete NaN and reindex
#
#         return self.pr_df
#
#     #  Count the lest frequent words
#     def count_rare_word(self):
#         freq = pd.Series(" ".join(self.pr_df).split()).value_counts()[-15:]
#         return freq
#
#     # Remove rare words - To use if necessary
#     def remove_rare_words(self):
#         freq = pd.Series(" ".join(self.pr_df).split()).value_counts()[-15:]
#         freq = list(freq.index)
#         self.pr_df = self.pr_df.apply(
#             lambda x: " ".join(x for x in x.split() if x not in freq))
#
#         # Delete NaN and reindex:
#         self.pr_df = self.pr_df[.dropna().reset_index(
#             drop=True)
#         return self.pr_df
