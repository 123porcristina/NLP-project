from gensim.models import LdaModel
from gensim import corpora
import pandas as pd
from gensim.corpora import Dictionary
import gensim
from gensim.test.utils import datapath


class modelTopic:
    def __init__(self, doc):
        self.doc = doc
        self.temp_file = datapath("LDA_model")

    def model_year(self):
        lda = LdaModel.load(self.temp_file)
        df_year = (self.doc.groupby('year')['token_speech'].sum().reset_index())
        year_corpus = {}
        for idx, texto in enumerate(df_year.token_speech):
            text = texto
            dct = Dictionary([text])
            year_corpus.update({idx: ([dct.doc2bow(doc) for doc in [texto]])})
        df_year['bag_words'] = df_year.index.map(year_corpus)
        unseen_doc = df_year.bag_words[0]
        vector = lda[unseen_doc]  # get topic probability distribution for a document 2016

        return df_year#self.doc.groupby(['year']).sum().reset_index()

    def model_region(self):
        pass

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

    # def lda_model(self):
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
        lda_model = Lda(doc_term_matrix, num_topics=10, id2word=dct, passes=10)
        # print("LDa model show")
        # print(lda_model.show_topics())
        print("[INFO] Processing...")
        # print(lda_model.print_topics(num_topics=100, num_words=3))
        for idx, topic in lda_model.show_topics(num_topics=10, formatted=False, num_words=10):
            print('Topic: {} \tWords: {}'.format(idx, '|'.join([w[0] for w in topic])))

        """save the file for now"""
        lda_model.save(self.temp_file)

        # Load a potentially pretrained model from disk.
        # lda = LdaModel.load(temp_file)


        return lda_model
