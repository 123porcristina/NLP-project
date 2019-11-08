from gensim.models import LdaModel
from gensim import corpora
import pandas as pd
from gensim.corpora import Dictionary
import gensim


class modelTopic:
    def __init__(self, doc):
        self.doc = doc

    def lda_model(self):
        conv_df = pd.DataFrame(list(self.doc.items()), columns=['id', 'speech'])
        texts = conv_df.speech
        dct = Dictionary(texts)
        print(dct)

        """converts speech to bag of words"""
        doc_term_matrix = [dct.doc2bow(doc) for doc in conv_df.speech]

        """instance the model"""
        Lda = gensim.models.ldamodel.LdaModel
        lda_model = Lda(doc_term_matrix, num_topics=100, id2word=dct, passes=50)
        # print("LDa model show")
        # print(lda_model.show_topics())
        print("[INFO] Processing...")
        # print(lda_model.print_topics(num_topics=100, num_words=3))
        for idx, topic in lda_model.show_topics(num_topics=100, formatted=False, num_words=10):
            print('Topic: {} \tWords: {}'.format(idx, '|'.join([w[0] for w in topic])))
