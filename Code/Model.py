from gensim.models import LdaModel
from gensim import corpora
import pandas as pd
from gensim.corpora import Dictionary
import gensim


class modelTopic:
    def __init__(self, doc):
        self.doc = doc

    def model_year(self):
        df_year = self.doc.groupby(['year']).sum().reset_index()
        for index, row in df_year.iterrows():
            # speech = row['token_speech']
            df_year['model'] = self.lda_model(row)
        # df_year['model'] = df_year.apply(lambda row: self.lda_model(row), axis=1) #it changes the data type so it is bad

        # self.lda_model(df=df_year)
        return df_year#self.doc.groupby(['year']).sum().reset_index()

    def model_region(self):
        pass

    def model_population(self):
        pass

    # def lda_model(self):
    def lda_model(self, df):
        texts = df.token_speech#self.doc.token_speech
        dct = Dictionary(texts)
        print(dct)

        """Remove High Frequent and Low Frequent Words"""
        dct.filter_extremes(no_below=20, no_above=0.5)

        """converts speech to bag of words"""
        # doc_term_matrix = [dct.doc2bow(doc) for doc in conv_df.speech]
        # doc_term_matrix = [dct.doc2bow(doc) for doc in self.doc.token_speech]
        # doc_term_matrix = [dct.doc2bow(doc) for doc in df.token_speech]
        corpus = [dct.doc2bow(doc) for doc in df.token_speech]

        """instance the model"""
        Lda = gensim.models.ldamodel.LdaModel
        # lda_model = Lda(doc_term_matrix, num_topics=10, id2word=dct, passes=10)
        lda_model = Lda(corpus, num_topics=10, id2word=dct, passes=10)
        # print("LDa model show")
        # print(lda_model.show_topics())
        print("[INFO] Processing...")
        # print(lda_model.print_topics(num_topics=100, num_words=3))
        for idx, topic in lda_model.show_topics(num_topics=10, formatted=False, num_words=3):
            print('Topic: {} \tWords: {}'.format(idx, '|'.join([w[0] for w in topic])))



        return lda_model
