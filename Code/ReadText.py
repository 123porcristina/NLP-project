from os import listdir
from os.path import isfile, join
from nltk.tokenize import TreebankWordTokenizer
import docx

# nltk.download('punkt')
# nltk.download('stopwords')


class ReadDoc:
    def __init__(self, directory, type_doc):
        self.directory = directory
        self.type_doc = type_doc

    def read_directory_files(self):
        """Get documents from the directory"""
        file_texts = []
        files = [f for f in listdir(self.directory) if isfile(join(self.directory, f))]
        for f in files: #maybe here we can do a validation type doc
            file_text = self.getTextDoc(join(self.directory, f))
            # print(file_text)
            file_texts.append({"file": f, "content": file_text})
        return file_texts

    def getTextDoc(self, filename):
        """Read text from documents"""
        doc = docx.Document(filename)
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        return '\n'.join(fullText)

    def getTextPDF(self, filename):
        pass
