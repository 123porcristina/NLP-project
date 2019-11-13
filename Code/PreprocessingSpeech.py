from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS
from collections import defaultdict
import string
nlp = English()
import en_core_web_sm
nlp2 = en_core_web_sm.load()


class Preprocessing:

    def __init__(self, speeches):
        self.speeches = speeches

    def clean_data(self):
        tokens = {}
        for index, row in self.speeches.iterrows():
            speech = row['speech']
            token_word = self.tokenize_word(speech)
            filtered_word = self.remove_words(token_word)
            filtered_entities = self.remove_entities(filtered_word)
            tokens.update({index: filtered_entities})
            self.speeches['token_speech'] = self.speeches.index.map(tokens)
        return self.speeches

    @staticmethod
    def tokenize_word(document):
        token_list = []
        try:
            words = nlp(document)
            [token_list.append(token.lemma_) for token in words if len(token) > 2 and token.text != '\n'
             and not token.is_stop and not token.is_punct and not token.like_num]
        except Exception as e:
            pass  # print("Error in tokenize_word process", e)
        return token_list

    @staticmethod
    def remove_words(word_list):
        stopwords = STOP_WORDS
        # nlc_stopwords = [u'welcome', u'Welcome', u'thank', u'Thank', u'thanks', u'words', u'thanking', u'let', u'like',
        #                  u'lot', u'Good', u'good', u'morning', u'afternoon', u'evening', u'look', u'honor', u'tonight',
        #                  u'city', u'today', u'state', u'january', u'february', u'feb', u'march', u'june', u'july',
        #                  u'august', u'september', u'october', u'november', u'december', u'monday', u'tuesday',
        #                  u'wednesday', u'thursday', u'friday', u'saturday', u'sunday', u'presentation', u'community',
        #                  u'new', u'year', u'years', u'th', u'applause']
        punctuations = string.punctuation
        filtered_list = []

        [filtered_list.append(token) for token in word_list if len(token) > 1 and token.lower() not in stopwords
         and token.isalpha() and token not in punctuations]  # and token not in nlc_stopwords]
        return filtered_list

    @staticmethod
    def remove_entities(filtered_word):
        filtered_entities = []
        doc = nlp2(str(filtered_word))
        entities = ([X.text for X in doc.ents])
        filtered_entities += ([word for word in filtered_word if word not in entities])
        return filtered_entities
