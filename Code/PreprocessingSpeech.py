from spacy.lang.en.stop_words import STOP_WORDS
import string
# import en_core_web_sm
import en_core_web_lg
import time
import pandas as pd

# nlp = en_core_web_sm.load()
nlp = en_core_web_lg.load()


class Preprocessing:

    def __init__(self, speeches):
        self.speeches = speeches

    def clean_data(self):
        start = time.time()
        tokens = {}
        for row in self.speeches.itertuples():
            token_word = self.tokenize_word(row.speech, allowed_postags=['NOUN', 'ADJ', 'VERB'])
            filtered_word = self.remove_words(token_word)
            filtered_entities = self.remove_entities(filtered_word)
            tokens.update({row. Index: filtered_entities})
        self.speeches['token_speech'] = self.speeches.index.map(tokens)
        end = time.time()
        print("[INFO]... Time preprocessing: " +str((end - start)*1000))
        return self.speeches

    def add_regions(self):
        regions = pd.read_csv('https://raw.githubusercontent.com/cphalpert/census-regions/master/us%20census%20bureau%20regions%20and%20divisions.csv')
        self.speeches = pd.merge(self.speeches, regions, how='left', left_on='state', right_on='State Code')
        self.speeches = self.speeches.drop(['State', 'State Code', 'Division'], axis=1)
        self.speeches = self.speeches[["city", "state", "Region", "year", "type_doc", "speech"]]

    @staticmethod
    def tokenize_word(document, allowed_postags=['NOUN', 'ADJ', 'VERB']):
        token_list = []
        try:
            words = nlp(document)
            [token_list.append(token.lemma_) for token in words if len(token) > 2 and token.text != '\n'
             and not token.is_stop and not token.is_punct and not token.like_num and token.pos_ in allowed_postags]
        except Exception as e:
            pass  # print("Error in tokenize_word process", e)
        return token_list

    @staticmethod
    def remove_words(word_list):
        stopwords = STOP_WORDS
        nlc_stopwords = [u'welcome', u'Welcome', u'thank', u'Thank', u'thanks', u'words', u'thanking', u'let', u'like',
                         u'lot', u'Good', u'good', u'morning', u'afternoon', u'evening', u'look', u'honor', u'tonight',
                         u'city', u'today', u'state', u'January', u'february', u'feb', u'March', u'June', u'july',
                         u'august', u'september', u'october', u'november', u'December', u'monday', u'tuesday',
                         u'wednesday', u'thursday', u'friday', u'saturday', u'sunday', u'presentation', u'community',
                         u'new', u'year', u'years', u'th', u'applause', u'ity', u'fall', u'Spring', u'summer', u'New',
                         u'council', u'San', u'talk', u'love', u'county', u'Councilmember', u'Town', u'town', u'West',
                         u'announce', u'President', u'president', u'percent', u'tell', u'feel', u'page', u'try',
                         u'little', u'initiative', u'aim', u'agree', u'hear', u'choose', u'region', u'turn', u'fact',
                         u'key', u'mean', u'example', u'mayor', u'follow', u'awards', u'award', u'idea']
        punctuations = string.punctuation
        filtered_list = []

        [filtered_list.append(token.casefold()) for token in word_list if len(token) > 2 and token.lower() not in stopwords
         and token.isalpha() and token not in punctuations and token not in nlc_stopwords]
        return filtered_list

    @staticmethod
    def remove_entities(filtered_word):
        filtered_entities = []
        doc = nlp(str(filtered_word))
        # entities = ([X.text for X in doc.ents])
        entities = ['PERSON', 'NORP', 'GPE', 'LOC', 'WORK_OF_ART', 'DATE', 'TIME', 'ORDINAL', 'CARDINAL']
        filtered_entities += ([word for word in filtered_word if word not in entities])
        return filtered_entities
