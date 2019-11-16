# Here is some sample code for preprocessing on a different data set:




# Importing and Download Sample Data
import io
import os.path
import re
import tarfile
import smart_open

def extract_documents(url='https://cs.nyu.edu/~roweis/data/nips12raw_str602.tgz'):
    fname = url.split('/')[-1]

    if not os.path.isfile(fname):
        with smart_open.open(url, "rb") as fin:
            with smart_open.open(fname, 'wb') as fout:
                while True:
                    buf = fin.read(io.DEFAULT_BUFFER_SIZE)
                    if not buf:
                        break
                    fout.write(buf)
                         
    with tarfile.open(fname, mode='r:gz') as tar:
        # Ignore directory entries, as well as files like README, etc.
        files = [
            m for m in tar.getmembers()
            if m.isfile() and re.search(r'nipstxt/nips\d+/\d+\.txt', m.name)
        ]
        for member in sorted(files, key=lambda x: x.name):
            member_bytes = tar.extractfile(member).read()
            yield member_bytes.decode('utf-8', errors='replace')

docs = list(extract_documents())


### Here checking the length of the documents

print(len(docs))
print(docs[0][0:500])


## Turn Documents into Spacy Objects


import spacy
nlp = spacy.load('en_core_web_sm')
docs1= []
for document in docs[0:50]:
    document = nlp(document)
    docs1.append(document)
print(len(docs1))


## Remove: Stop Words, Words 1 digit or less, punctation, and numbers
## Turn Document into a list of lemmas

for idx in range(len(docs1)):
    text=[]
    for w in docs1[idx]:
        if len(w) > 1 and not w.is_stop and not w.is_punct and not w.like_num:
            text.append(w.lemma_)
    docs1[idx] = text

print(len(docs1[1]))
print(docs1[0])


##Add Frequent Bigrams

from gensim.models import Phrases
bigram = Phrases(docs1, min_count=20)
for idx in range(len(docs1)):
    for token in bigram[docs1[idx]]:
        if '_' in token:
            # Token is a bigram, add to document.
            docs1[idx].append(token)


print(docs1[0])

## Remove High Frequent and Low Frequent Words

from gensim.corpora import Dictionary
dictionary = Dictionary(docs1)
dictionary.filter_extremes(no_below=20, no_above=0.5)


## Turn documents into bag of words vector

corpus = [dictionary.doc2bow(doc) for doc in docs1]


## Check the Number of Words and Number of Documents


print('Number of unique tokens: %d' % len(dictionary))
print('Number of documents: %d' % len(corpus))


### Build LDA Model


from gensim.models import LdaModel
num_topics = 10
chunksize = 2000
passes = 20
iterations = 400
eval_every = None
temp = dictionary[0] 
id2word = dictionary.id2token
model = LdaModel(
    corpus=corpus,
    id2word=id2word,
    chunksize=chunksize,
    alpha='auto',
    eta='auto',
    iterations=iterations,
    num_topics=num_topics,
    passes=passes,
    eval_every=eval_every
)


## Print the top topics

top_topics = model.top_topics(corpus)

from pprint import pprint
pprint(top_topics)


# Apply Model to one document to get the topic distribution

model[corpus[0]]


model.show_topics()[2]

# Visualization of Topic MOde

import pyLDAvis.gensim
pyLDAvis.enable_notebook()
vis = pyLDAvis.gensim.prepare(model, corpus, dictionary)
vis


# Websites with more info on
# https://nbviewer.jupyter.org/github/bmabey/pyLDAvis/blob/master/notebooks/pyLDAvis_overview.ipynb
#
# https://liferay.de.dariah.eu/tatom/topic_model_visualization.html



