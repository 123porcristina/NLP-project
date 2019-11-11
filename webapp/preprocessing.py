# from docx import Document
import PyPDF2
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS
import string
import csv
from pathlib import Path

dir_base = (str(Path(__file__).parents[1]))
print(dir_base)

nlp = English()


def save_to_csv(file, csv_file):
    pdfFileObj = open((file), 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict=False, overwriteWarnings=True)
    num_pages = pdfReader.numPages
    count = 0
    pdf_text = ""
    while count < num_pages:
        try:
            pageObj = pdfReader.getPage(count)
            pdf_text += (pageObj.extractText()).casefold()
            count += 1
        except Exception as e:
            # print(("BAD FILE: ", pageObj, ' - ', root, file_))
            print("PDF failed to read. Error is: ", e)
            return

    token_list = []
    try:
        words = nlp(pdf_text)
        [token_list.append(token.lemma_) for token in words]
    except Exception as e:
        print("Error in tokenize_word process", e)

    stopwords = STOP_WORDS
    nlc_stopwords = [u'welcome', u'Welcome', u'thank', u'Thank', u'thanks', u'words', u'thanking', u'let', u'like',
                     u'lot', u'Good', u'good', u'morning', u'afternoon', u'evening', u'look', u'honor', u'tonight',
                     u'city', u'today', u'state', u'january', u'february', u'feb', u'march', u'june', u'july',
                     u'august', u'september', u'october', u'november', u'december', u'monday', u'tuesday',
                     u'wednesday', u'thursday', u'friday', u'saturday', u'sunday', u'presentation', u'community',
                     u'new', u'year', u'years', u'th', u'applause']

    punctuations = string.punctuation
    filtered_list = []
    [filtered_list.append(token) for token in token_list if token.lower() not in stopwords and token.isalpha()
     and token not in punctuations and token not in nlc_stopwords]

    with open(csv_file, 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(filtered_list)


file_path = dir_base + '/webapp/uploads/New_York_NY_final.pdf'
csv_file_path = dir_base + '/webapp/processed_files/New_York_NY_final.csv'

save_to_csv(file_path, csv_file_path)