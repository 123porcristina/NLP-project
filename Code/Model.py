# from gensim.models import LdaModel
from gensim.models.ldamodel import LdaModel
import pandas as pd
from gensim.corpora import Dictionary
import gensim
from gensim.test.utils import datapath
from gensim.models.coherencemodel import CoherenceModel
import warnings

warnings.filterwarnings('ignore')  # To ignore all warnings that arise here to enhance clarity
# import logging  # This allows for seeing if the model converges. A log file is created.

# logging.basicConfig(filename='lda_model.log', format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class ModelTopic:
    def __init__(self, doc):
        self.doc = doc
        self.temp_file = datapath("LDA_model")

    def model_year(self):
        """dataframe grouped by year"""
        # df_year = (self.doc.groupby('year')['token_speech'].sum().reset_index())
        df_year = (self.doc.groupby('year')['combined'].sum().reset_index())

        """Applies LDA model"""
        df_year = self.model_unseen(df_year)

        return df_year  # self.doc.groupby(['year']).sum().reset_index()

    def model_region(self):
        """dataframe grouped by region"""
        # df_region = (self.doc.groupby('Region')['token_speech'].sum().reset_index())
        df_region = (self.doc.groupby('Region')['combined'].sum().reset_index())

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
            try:  # row 16 does not exist. Maybe the pickle is corrupt? check!!!
                [bi_token.append(token) for token in bigram[self.doc.token_speech[idx]] if '_' in token]
                bi_word.update({idx: bi_token})
                bi_token = []
            except:
                pass
        self.doc['bigram_speech'] = self.doc.index.map(bi_word)
        self.doc['combined'] = (self.doc.bigram_speech + self.doc.token_speech)
        # print("Printing bigrams")
        # print('\n'.join('{}: {}'.format(*k) for k in enumerate(self.doc.bigram_speech)))

        ##test to know frequency
        from collections import Counter
        words = self.doc.token_speech.sum()
        word_freq = Counter(words)
        common_words = word_freq.most_common(200)
        # print("Most frequent tokens:")
        # print(common_words)

        words = self.doc.bigram_speech.sum()
        word_freq = Counter(words)
        common_words = word_freq.most_common(200)
        # print("Most frequent BIGRAMS:")
        # print(common_words)
        return self.doc.bigram_speech, common_words
        ###

    def lda_model(self, num_topics, chunksize, alpha, eta, passes):
        texts = self.doc['combined'].dropna()
        # texts=self.doc.bigram_speech.dropna() #
        dct = Dictionary(texts)

        """Remove High Frequent and Low Frequent Words"""
        # Filter out words that occur less than 1 documents, or more than 50% of the documents.
        dct.filter_extremes(no_below=5, no_above=0.5)

        """converts speech to bag of words"""
        doc_term_matrix = [dct.doc2bow(doc) for doc in texts]

        """instance the model"""
        Lda = gensim.models.ldamodel.LdaModel
        lda_model = Lda(doc_term_matrix, num_topics=num_topics, id2word=dct,
                        random_state=1,
                        chunksize=chunksize,
                        alpha=alpha,
                        eta=eta,
                        iterations=400,
                        passes=passes,
                        eval_every=None
                        )

        print("[INFO] Processing Topics...")
        for idx, topic in lda_model.show_topics(num_topics=num_topics, formatted=False, num_words=15):
            print('Topic: {} \tWords: {}'.format(idx, '|'.join([w[0] for w in topic])))

        """save the file for now"""
        lda_model.save(self.temp_file)

        """Coherence Score"""
        coherence_model_lda = CoherenceModel(model=lda_model, texts=texts, dictionary=dct, coherence='c_v')
        coherence_lda = coherence_model_lda.get_coherence()
        # print('\nCoherence Score: ', coherence_lda)

        import pyLDAvis.gensim
        vis = pyLDAvis.gensim.prepare(lda_model, doc_term_matrix, dct, R=15, mds='mmds')
        # # pyLDAvis.show(vis)
        pyLDAvis.save_html(vis, '../App v2/assets/lda.html')

        return lda_model, coherence_lda, doc_term_matrix, texts

    def format_topics_sentences(self, ldamodel, corpus, texts): #texts):  def format_topics_sentences(ldamodel=lda_model, corpus=doc_term_matrix, texts=texts):
        # Init output
        sent_topics_df = pd.DataFrame()

        # Get main topic in each document
        for i, row in enumerate(ldamodel[corpus]):
            row = sorted(row, key=lambda x: (x[1]), reverse=True)
            # Get the Dominant topic, Perc Contribution and Keywords for each document
            for j, (topic_num, prop_topic) in enumerate(row):
                if j == 0:  # => dominant topic
                    wp = ldamodel.show_topic(topic_num)
                    topic_keywords = ", ".join([word for word, prop in wp])
                    sent_topics_df = sent_topics_df.append(
                        pd.Series([int(topic_num), round(prop_topic, 4), topic_keywords]), ignore_index=True)
                else:
                    break
        sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

        # Add original text to the end of the output
        contents = pd.Series(texts)
        sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
        # Format
        df_dominant_topic = sent_topics_df.reset_index()
        df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']
        df_dominant_topic.to_csv('dominant_topic.csv')
        print(df_dominant_topic.head(10))
        return df_dominant_topic, sent_topics_df


    # Group top 5 sentences under each topic
    def top_five(self, sent_topics_df):

        sent_topics_sorted = pd.DataFrame()
        sent_topics_outdf_grpd = sent_topics_df.groupby('Dominant_Topic')

        for i, grp in sent_topics_outdf_grpd:
            sent_topics_sorted = pd.concat([sent_topics_sorted,
                                            grp.sort_values(['Perc_Contribution'], ascending=[0]).head(1)], axis=0)

        # Reset Index
        sent_topics_sorted.reset_index(drop=True, inplace=True)

        # Format
        sent_topics_sorted.columns = ['Topic_Num', "Topic_Perc_Contrib", "Keywords", "Text"]

        # Show
        sent_topics_sorted.to_csv('sent_topics.csv')
        print(sent_topics_sorted.head())

        # Number of Documents for Each Topic
        topic_counts = sent_topics_df['Dominant_Topic'].value_counts()

        # Percentage of Documents for Each Topic
        topic_contribution = round(topic_counts / topic_counts.sum(), 4)

        # Topic Number and Keywords
        topic_num_keywords = sent_topics_df[['Dominant_Topic', 'Topic_Keywords']]

        # Concatenate Column wise
        df_dominant_topics = pd.concat([topic_num_keywords, topic_counts, topic_contribution], axis=1)

        # Change Column names
        df_dominant_topics.columns = ['Dominant_Topic', 'Topic_Keywords', 'Num_Documents', 'Perc_Documents']

        # Show
        df_dominant_topics.to_csv('dominant_topic_sorted.csv')
        print(df_dominant_topics)

        return df_dominant_topics

    def model_unseen(self, df):
        lda = LdaModel.load(self.temp_file)
        # import pyLDAvis.gensim
        """Runs LDA for each year and save it"""
        corpus = {}
        for idx, doc in enumerate(df.combined):
            # dct = Dictionary(doc)
            doc_vector = lda.id2word.doc2bow(doc)
            corpus.update({idx: lda[doc_vector]})
            # [[(id2word[id], freq) for id, freq in cp] for cp in corpus[:1]]
            # vis = pyLDAvis.gensim.prepare(lda, doc_vector, dct, R=15)
            # pyLDAvis.show(vis)

        df['lda'] = df.index.map(corpus)
        print("\n".join("{}\t{}".format(k, v) for k, v in corpus.items()))
        return df
