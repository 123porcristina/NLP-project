# from gensim.models import LdaModel
from gensim.models.ldamodel import LdaModel
import pandas as pd
from gensim.corpora import Dictionary
import gensim
from gensim.test.utils import datapath
from gensim.models.coherencemodel import CoherenceModel
import warnings
warnings.filterwarnings('ignore')  # To ignore all warnings that arise here to enhance clarity
import logging # This allows for seeing if the model converges. A log file is created.
# logging.basicConfig(filename='lda_model.log', format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class ModelTopic:
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
        df_region = (self.doc.groupby('Region')['token_speech'].sum().reset_index())

        """Applies LDA model"""
        df_region = self.model_unseen(df_region)
        return df_region

    def model_population(self):
        pass

    def model_bigram(self):
        bi_token = []
        bi_word = {}
        bigram = gensim.models.Phrases(self.doc['token_speech'])
        for idx in range(len(self.doc['token_speech'])):
            try:#row 16 does not exist. Maybe the pickle is corrupt? check!!!
                [bi_token.append(token) for token in bigram[self.doc.token_speech[idx]] if '_' in token]
                bi_word.update({idx: bi_token})
                bi_token = []
            except:
                pass
        self.doc['bigram_speech'] = self.doc.index.map(bi_word)
        print("Printing bigrams")
        print('\n'.join('{}: {}'.format(*k) for k in enumerate(self.doc.bigram_speech)))


    def lda_model(self):

        self.doc['combined'] = (self.doc.bigram_speech + self.doc.token_speech) #(self.doc.token_speech + self.doc.bigram_speech)
        # texts = self.doc['combined'].dropna()
        texts=self.doc.bigram_speech.dropna() #
        dct = Dictionary(texts)

        """Remove High Frequent and Low Frequent Words"""
        dct.filter_extremes(no_below=5, no_above=0.5)

        """converts speech to bag of words"""
        doc_term_matrix = [dct.doc2bow(doc) for doc in texts]

        """instance the model"""
        Lda = gensim.models.ldamodel.LdaModel
        lda_model = Lda(doc_term_matrix, num_topics=80, id2word=dct)

        print("[INFO] Processing Topics...")
        for idx, topic in lda_model.show_topics(num_topics=80, formatted=False, num_words=15):
            print('Topic: {} \tWords: {}'.format(idx, '|'.join([w[0] for w in topic])))

        """save the file for now"""
        lda_model.save(self.temp_file)

        """Coherence Score"""
        coherence_model_lda = CoherenceModel(model=lda_model, texts=texts, dictionary=dct, coherence='c_v')
        coherence_lda = coherence_model_lda.get_coherence()
        print('\nCoherence Score: ', coherence_lda)

        # import pyLDAvis.gensim
        # vis = pyLDAvis.gensim.prepare(lda_model, doc_term_matrix, dct, R=15)
        # # pyLDAvis.display(vis)
        # pyLDAvis.show(vis)

        return lda_model

    def model_unseen(self, df):
        lda = LdaModel.load(self.temp_file)
        import pyLDAvis.gensim
        """Runs LDA for each year and save it"""
        year_corpus = {}
        for idx, doc in enumerate(df.token_speech):
            # dct = Dictionary(doc)
            doc_vector = lda.id2word.doc2bow(doc)
            year_corpus.update({idx: lda[doc_vector]})
            # [[(id2word[id], freq) for id, freq in cp] for cp in corpus[:1]]
            # vis = pyLDAvis.gensim.prepare(lda, doc_vector, dct, R=15)
            # pyLDAvis.show(vis)

        df['lda'] = df.index.map(year_corpus)
        print("\n".join("{}\t{}".format(k, v) for k, v in year_corpus.items()))
        return df
