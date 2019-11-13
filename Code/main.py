from Code import ReadText
from Code import PreprocessingSpeech as ps
from Code import Model
from pathlib import Path
import pandas as pd
pd.set_option('display.width', 2000)
pd.set_option('display.max_columns',10)

def main():
    dir_base = (str(Path(__file__).parents[1]) + '/Data')

    """Read PDFs and DOCs"""
    # readText = ReadText.ReadDoc(dir_base)
    # df_files = readText.read_directory_files()

    """Save the Dataframe structure locally into a pickle file to easiness of use"""
    # name = 'df_data'
    # save_df = ReadText.SaveDf(dir_base, df_files, name)
    # save_df.save_dataframe()

    """Read the pickle file"""
    # df_file = pd.read_pickle(dir_base+"/df_data.pickle")


    """Preprocessing texts"""
    # preprocessing = ps.Preprocessing(speeches=df_file)
    # clean_tokens = preprocessing.clean_data()

    """Save the new Dataframe structure locally into a pickle file to easiness of use"""
    # name = 'df_tokens'
    # save_df = ReadText.SaveDf(dir_base, clean_tokens, name)
    # save_df.save_dataframe()

    """Read the new Dataframe with the tokens"""
    df_tokens = pd.read_pickle(dir_base+"/df_tokens.pickle")
    print(df_tokens)
    print(df_tokens.loc[[1], ['token_speech']])

    """LDA Model"""
    # model = Model.modelTopic(doc=clean_tokens)
    # model.model_year()
    # model.lda_model()

    """Get the differences"""
    # differences = speech.getDifferences(tokenWord_base, tokenWord_curr)

    """Get the frequencies"""
    # doc_curr, frq_doc_base, frq_doc_curr = speech.plot(tokenWord_base, tokenWord_curr)

    """Probability distribution/high probability"""
    # mle_probab = speech.mle_distribution(doc_curr, frq_doc_base, frq_doc_curr)
    # doc_curr, freq_bi_curr, freq_bi_base, bigrams_doc, bigrams_base = speech.bigrams(tokenWord_base, tokenWord_curr)
    # high_prob_bigram = speech.mle_bigram(freq_bi_curr, freq_bi_base, bigrams_doc, len(tokenWord_curr))


main()




