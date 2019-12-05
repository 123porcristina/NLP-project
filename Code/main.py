from Code import ReadText
from Code import PreprocessingSpeech as ps
from Code import Model
from pathlib import Path
import pandas as pd

pd.set_option('display.width', 2000)
pd.set_option('display.max_columns', 10)


def main():
    dir_base = (str(Path(__file__).parents[1]) + '/Data')

    """Read PDFs and DOCs"""
    # print('[INFO]...Reading')
    # readText = ReadText.ReadDoc(dir_base)
    # df_files = readText.read_directory_files()

    """Save the Dataframe structure locally into a pickle file to easiness of use"""
    # name = 'df_data'
    # save_df = ReadText.SaveDf(dir_base, df_files, name)
    # save_df.save_dataframe()

    """Read the pickle file"""
    # print('[INFO]...Loading Pickle')
    # df_file = pd.read_pickle(dir_base+"/df_data.pickle")

    """Preprocessing texts"""
    # print('[INFO]...Preprocessing')
    # preprocessing = ps.Preprocessing(speeches=df_file)
    # preprocessing.add_regions()
    # clean_tokens = preprocessing.clean_data()
    # # print('\n'.join('{}: {}'.format(*k) for k in enumerate(clean_tokens)))

    """Save the new Dataframe structure locally into a pickle file to easiness of use"""
    # print('[INFO]...Saving Pickle')
    # name = 'df_tokens'
    # save_df = ReadText.SaveDf(dir_base, clean_tokens, name)
    # save_df.save_dataframe()

    """Read the new Dataframe with the tokens"""
    print('[INFO]...Reading pickle tokens')
    df_tokens = pd.read_pickle(dir_base + "/df_tokens.pickle")
    # print(df_tokens)

    """LDA Model"""
    print('[INFO]...Modeling')
    """Model over the whole data"""
    model = Model.ModelTopic(doc=df_tokens)
    model.model_bigram()
    lda_model, _, doc_term_matrix, texts = model.lda_model(num_topics=100, chunksize=100, alpha='auto', eta='auto', passes=200)
    
    """Apply model per year"""
    model.model_year()

    """Apply model per region"""
    # model.model_region()
    """most representative topics for each doc"""
    # _, sent_topics_df = model.format_topics_sentences(lda_model, doc_term_matrix, texts)
    # model.top_five(sent_topics_df=sent_topics_df)

    """Get the differences"""
    # differences = speech.getDifferences(tokenWord_base, tokenWord_curr)

    """Get the frequencies"""
    # doc_curr, frq_doc_base, frq_doc_curr = speech.plot(tokenWord_base, tokenWord_curr)

    """Probability distribution/high probability"""
    # mle_probab = speech.mle_distribution(doc_curr, frq_doc_base, frq_doc_curr)
    # doc_curr, freq_bi_curr, freq_bi_base, bigrams_doc, bigrams_base = speech.bigrams(tokenWord_base, tokenWord_curr)
    # high_prob_bigram = speech.mle_bigram(freq_bi_curr, freq_bi_base, bigrams_doc, len(tokenWord_curr))


if __name__ == '__main__':
    main()
