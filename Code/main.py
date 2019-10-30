from Code import ReadText
from Code import PreprocessingSpeech as ps
from pathlib import Path
import pandas as pd


def main():
    dir_base = (str(Path(__file__).parents[1]) + '/Data')

    """Read PDFs and DOCs"""
    readText = ReadText.ReadDoc(dir_base)
    df_files = readText.read_directory_files()
    print(df_files)

    """Save the Dataframe structure locally into a pickle file to easiness of use"""
    save_df = ReadText.SaveDf(dir_base, df_files)
    save_df.save_dataframe()


    """Read the pickle file"""
    #df_file = pd.read_pickle(dir_base+"/df_data.pickle")
    #print(df_file)
    #print(df_file.loc[3,'speech'])

    """Preprocessing texts"""
    # speech = ps.Preprocessing(base_speeches=base_speeches, curr_speeches=curr_speeches)
    # tokenWord_base = speech.tokenizeWord(base_speeches)
    # tokenWord_curr = speech.tokenizeWord(curr_speeches)

    """Get the differences"""
    # differences = speech.getDifferences(tokenWord_base, tokenWord_curr)

    """Get the frequencies"""
    # doc_curr, frq_doc_base, frq_doc_curr = speech.plot(tokenWord_base, tokenWord_curr)

    """Probability distribution/high probability"""
    # mle_probab = speech.mle_distribution(doc_curr, frq_doc_base, frq_doc_curr)
    # doc_curr, freq_bi_curr, freq_bi_base, bigrams_doc, bigrams_base = speech.bigrams(tokenWord_base, tokenWord_curr)
    # high_prob_bigram = speech.mle_bigram(freq_bi_curr, freq_bi_base, bigrams_doc, len(tokenWord_curr))


main()




