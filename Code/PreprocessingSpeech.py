from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS
import string

nlp = English()


class Preprocessing:

    def __init__(self, speeches):
        self.speeches = speeches

    def clean_data(self):
        tokens = {}
        for index, row in self.speeches.iterrows():
            speech = row['speech']
            tokenWord = self.tokenize_word(speech)
            filteredWord = self.remove_words(tokenWord)
            tokens.update({index: filteredWord})
        return print("the tokens are: \n", tokens)

    @staticmethod
    def tokenize_word(document):
        token_list = []
        try:
            words = nlp(document)
            [token_list.append(token.lemma_) for token in words]
        except Exception as e:
            print("Error in tokenize_word process", e)
        return token_list

    @staticmethod
    def remove_words(word_list):
        stopwords = STOP_WORDS
        nlc_stopwords = [u'welcome', u'Welcome', u'thank', u'Thank', u'thanks', u'words', u'thanking', u'let', u'like',
                         u'lot', u'Good', u'good', u'morning', u'afternoon', u'evening', u'look', u'honor', u'tonight',
                         u'city', u'today', u'state', u'january', u'february', u'feb', u'march', u'june', u'july',
                         u'august', u'september', u'october', u'november', u'december', u'monday', u'tuesday',
                         u'wednesday', u'thursday', u'friday', u'saturday', u'sunday', u'presentation', u'community',
                         u'new', u'year', u'years', u'th', u'applause']

        punctuations = string.punctuation
        filtered_list = []
        [filtered_list.append(token) for token in word_list if token.lower() not in stopwords and token.isalpha()
         and token not in punctuations and token not in nlc_stopwords]
        return filtered_list

    def remove_entities(self):
        pass