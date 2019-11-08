print("Test by Kanchan")

"""MISCELLANEOUS CODE FOR PREPROCESSINGSPEECH"""
# if filetype == '.docx':
#     for item in document:
#         words = nlp(item)
#         # # get rid of newlines
#         # words = words.strip().replace("\n", " ").replace("\r", " ")
#         [token_list.append(token.lemma_) for token in words]
#
# elif filetype == '.pdf':
#     try:
#         words = nlp(document)
#         [token_list.append(token.lemma_) for token in words]
#     except:
#         pass


# def getDifferences(self, wordListBase, wordListCurr):
#     return set(wordListCurr).difference(set(wordListBase))

# def getFrequency(self, wordListCurr, wordListBase):
#     return nltk.FreqDist(wordListCurr), nltk.FreqDist(wordListBase)


# def plot(self, frq_doc_base, frq_doc_curr):
#     """plot frequencies"""
#     doc_curr = self.remove_words(frq_doc_curr)
#     doc_base = self.remove_words(frq_doc_base)
#     frq_doc_curr, frq_doc_base = self.getFrequency(doc_curr, doc_base)
#     frq_doc_curr.plot(20), frq_doc_base.plot(20)
#     print('Most Common: ' + str(frq_doc_curr.most_common(20)))
#     # plt.show()
#     return doc_curr, frq_doc_base, frq_doc_curr

# def mle_distribution(self, doc_curr, frq_base, frq_curr):
#     high_probability_curr = []
#     mle_curr= nltk.MLEProbDist(frq_curr)
#     mle_base = nltk.MLEProbDist(frq_base)
#
#     print("MLE_jargon: "+str(mle_curr.prob('CEO, buildings')))
#
#     for token in doc_curr:
#         curr_prob = mle_curr.prob(token)
#         base_prob = mle_base.prob(token)
#         if curr_prob > base_prob:
#             high_probability_curr.append(token)
#     return high_probability_curr

# def bigrams(self, doc_base, doc_curr):
#     doc_curr = self.remove_words(doc_curr) #maybe put the remove method outside because it is being called twice
#     bigrams_doc = nltk.bigrams(doc_curr)
#     freq_bi_doc_curr = nltk.FreqDist(bigrams_doc)
#     print("Bigram current doc")
#     print(freq_bi_doc_curr.most_common(20))
#     freq_bi_doc_curr.plot(20)
#
#     print("Bigram Base doc")
#     doc_base = self.remove_words(doc_base)
#     bigrams_base = nltk.bigrams(doc_base)
#     freq_bi_base = nltk.FreqDist(bigrams_base)
#     print(freq_bi_base.most_common(20))
#     freq_bi_base.plot(20)
#
#     return doc_curr, freq_bi_doc_curr, freq_bi_base, bigrams_doc, bigrams_base

# def mle_bigram(self, freq_bi_curr, freq_bi_base, bigrams_doc, word_length):
#     high_probabilty_bigram = []
#     Smoothed_dist_curr = nltk.LaplaceProbDist(freq_bi_curr)
#     Smoothed_dist_base = nltk.LaplaceProbDist(freq_bi_base)
#     print(Smoothed_dist_curr.prob(('DoD', 'Test')))
#     print(Smoothed_dist_curr.logprob(('Chair', 'Force')))
#     print(Smoothed_dist_curr.generate())
#
#     slogprob = 0
#     for bigram_words in bigrams_doc:
#         logprob_curr = Smoothed_dist_curr.logprob(bigram_words)
#         slogprob += logprob_curr
#         logprob_base = Smoothed_dist_base.logprob(bigram_words)
#         if logprob_curr > logprob_base:
#             high_probabilty_bigram.append(bigram_words)
#
#     return high_probabilty_bigram #slogprob / word_length
