from gensim.models import LdaModel
from gensim import corpora
import pandas as pd
from gensim.corpora import Dictionary
import gensim
from gensim.test.utils import datapath
import logging # This allows for seeing if the model converges. A log file is created.
# logging.basicConfig(filename='lda_model.log', format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class modelTopic:
    def __init__(self, doc):
        self.doc = doc
        self.temp_file = datapath("LDA_model")

    def model_year(self):
        """dataframe grouped by year"""
        df_year = (self.doc.groupby('year')['token_speech'].sum().reset_index())

        """Applies LDA model"""
        df_year = self.model_unseen(df_year)

        return df_year#self.doc.groupby(['year']).sum().reset_index()

    def model_region(self):
        """dataframe grouped by year"""
        df_region = (self.doc.groupby('region')['token_speech'].sum().reset_index())

        """Applies LDA model"""
        df_region = self.model_unseen(df_region)
        return df_region

    def model_population(self):
        pass

    def model_bigram(self):
        #Move this section to preprocessing but overthere it gives problems. check!!!
        bi_token = []
        bi_word = {}
        bigram = gensim.models.Phrases(self.doc['token_speech'], min_count=5)
        for idx in range(len(self.doc['token_speech'])):
            try:#row 16 does not exist. Maybe the pickle is corrupt? check!!!
                [bi_token.append(token) for token in bigram[self.doc.token_speech[idx]] if '_' in token]
                bi_word.update({idx: bi_token})
                bi_token = []
            except:
                pass
        self.doc['bigram_speech'] = self.doc.index.map(bi_word)
        print("Bigrams")
        print('\n'.join('{}: {}'.format(*k) for k in enumerate(self.doc.bigram_speech)))

    def lda_model(self, df):
        texts = df.token_speech#self.doc.token_speech
        dct = Dictionary(texts)
        print(dct)

        """Remove High Frequent and Low Frequent Words"""
        dct.filter_extremes(no_below=20, no_above=0.5)

        """converts speech to bag of words"""
        doc_term_matrix = [dct.doc2bow(doc) for doc in df.token_speech]
        # corpus = [dct.doc2bow(doc) for doc in df.token_speech]

        """instance the model"""
        Lda = gensim.models.ldamodel.LdaModel
        lda_model = Lda(doc_term_matrix, num_topics=10, id2word=dct, passes=10, iterations=400,
                        eval_every=None, chunksize=2000)
        # print("LDa model show")
        # print(lda_model.show_topics())
        print("[INFO] Processing...")
        # print(lda_model.print_topics(num_topics=100, num_words=3))
        for idx, topic in lda_model.show_topics(num_topics=10, formatted=False, num_words=10):
            print('Topic: {} \tWords: {}'.format(idx, '|'.join([w[0] for w in topic])))

        """save the file for now"""
        lda_model.save(self.temp_file)

        return lda_model

    def model_unseen(self, df):
        lda = LdaModel.load(self.temp_file)

        """Runs LDA for each year and save it"""
        year_corpus = {}
        for idx, doc in enumerate(df.token_speech):
            doc_vector = lda.id2word.doc2bow(doc)
            year_corpus.update({idx: lda[doc_vector]})

        df['lda'] = df.index.map(year_corpus)
        print("\n".join("{}\t{}".format(k, v) for k, v in year_corpus.items()))
        return df

