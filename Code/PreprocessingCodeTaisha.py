# These are steps for preprocessing that I got from my NLP book and the Gensim Website. I think we should follow
# steps before running the LDA model again



#Step1: Lemmatize. Remove: stop words, numbers, punctution, and words with only 1 digit
for document in documents:
    text = []
    doc = nlp(document)
    for w in doc:
        if len(w) > 1 and not w.is_stop and not w.is_punct and not w.like_num :
            text.append(w.lemma_)
    texts.append(text)

#Step2: Add Bigrams to our list of words if they occur more than 10 times, we can adjust the number
from gensim.models import Phrases

bigram = Phrases(docs, min_count=20)
for idx in range(len(docs)):
    for token in bigram[docs[idx]]:
        if '_' in token:
            # Token is a bigram, add to document.
            docs[idx].append(token)

#Step3: Remove rare and common words based on their frequency in each document

from gensim.corpora import Dictionary

# Create a dictionary representation of the documents.
dictionary = Dictionary(docs)

# Filter out words that occur less than 20 documents, or more than 50% of the documents.
dictionary.filter_extremes(no_below=20, no_above=0.5)


#Step5: Transform to a Bag of Words

corpus = [dictionary.doc2bow(doc) for doc in docs]