from Code import ReadText
from Code import PreprocessingSpeech as ps


def main():
    dir_base = 'C:/Users/Giraldo/Documents/NLC/NLP/Data/Base Data'
    dir_curr = 'C:/Users/Giraldo/Documents/NLC/NLP/Data/Current Data'

    """Read texts"""
    readText = ReadText.ReadDoc(directory=dir_base, type_doc='docx')
    base_speeches = readText.read_directory_files()
    readText = ReadText.ReadDoc(directory=dir_curr, type_doc='docx')
    curr_speeches = readText.read_directory_files()

    """Preprocessing texts"""
    speech = ps.Preprocessing(base_speeches=base_speeches, curr_speeches=curr_speeches)
    tokenWord_base = speech.tokenizeWord(base_speeches)
    tokenWord_curr = speech.tokenizeWord(curr_speeches)

    """Get the differences"""
    differences = speech.getDifferences(tokenWord_base, tokenWord_curr)

    """Get the frequencies"""
    doc_curr, frq_doc_base, frq_doc_curr = speech.plot(tokenWord_base, tokenWord_curr)

    """Probability distribution/high probability"""
    mle_probab = speech.mle_distribution(doc_curr, frq_doc_base, frq_doc_curr)
    doc_curr, freq_bi_curr, freq_bi_base, bigrams_doc, bigrams_base = speech.bigrams(tokenWord_base, tokenWord_curr)
    high_prob_bigram = speech.mle_bigram(freq_bi_curr, freq_bi_base, bigrams_doc, len(tokenWord_curr))

main()
