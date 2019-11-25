from os import walk
from docx import Document
import PyPDF2
import os
import pandas as pd
import re


class ReadDoc:
    def __init__(self, path):
        self.path = path

    def read_directory_files(self):
        df_files = pd.DataFrame(columns=['city', 'state', 'year', 'type_doc', 'speech'])

        """RC. Iterate over each folder to find possible .PDFs and .DOCX documents. also"""
        for root, dirs, files in walk(self.path):
            for file_ in files:
                if file_.endswith('.docx'):
                    doc_text = ReadDoc.get_text_doc(root, file_)
                    city_text = re.split(', |\(', file_)[0]
                    state_text = re.search('[A-Z]+[A-Z]', file_)[0]
                    year_text = re.findall(r'.*([1-3][0-9]{3})', (os.path.join(root, file_)))[0]
                    df_files = df_files.append({'city': city_text,
                                                'state': state_text,
                                                'year': year_text,
                                                'type_doc': '.docx',
                                                'speech': doc_text}, ignore_index=True)

                elif file_.endswith('.pdf'):
                    pdf_text = ReadDoc.get_text_pdf(root, file_)
                    city_text = re.split(', |\(', file_)[0]
                    state_text = re.search('[A-Z]+[A-Z]', file_)[0]
                    year_text = re.findall(r'.*([1-3][0-9]{3})', (os.path.join(root, file_)))[0]
                    df_files = df_files.append({'city': city_text,
                                                'state': state_text,
                                                'year': year_text,
                                                'type_doc': '.pdf',
                                                'speech': pdf_text}, ignore_index=True)

        """
        Temporarily, we are deleting the rows that are empty. We need to solve how to read properly 
        all the PDF files.
        """
        df_files['speech'] = df_files['speech'].astype(str)
        df_files = df_files[df_files.speech != ""]
        df_files = df_files.reset_index(drop=True)

        return df_files

    """RC. This function looks for all the .DOCX documents and return just the text for each document"""
    @staticmethod
    def get_text_doc(root, file_):
        doc = Document((os.path.join(root, file_)))
        #doc_text = []
        doc_text = ""
        for para in doc.paragraphs:
            #doc_text.append(para.text.casefold())
            doc_text += para.text#.casefold()
        return doc_text

    """RC. This function looks for all the .PDF documents and return just the text for each document"""
    @staticmethod
    def get_text_pdf(root, file_):
        pdfFileObj = open((os.path.join(root, file_)), 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict=False, overwriteWarnings=True)
        num_pages = pdfReader.numPages
        count = 0
        pdf_text = ""
        while count < num_pages:
            try:
                pageObj = pdfReader.getPage(count)
                pdf_text += (pageObj.extractText())#.casefold()
                count += 1
            except Exception as e:
                print("file : ", root, file_, " -- Error: ", e)
                return
        return pdf_text


class SaveDf:
    def __init__(self, dir_base, df_files, df_name):
        self.dir_base = dir_base
        self.df_files = df_files
        self.df_name = df_name

    def save_dataframe(self):
        data_df = pd.DataFrame(self.df_files)
        return data_df.to_pickle(self.dir_base+'/' + self.df_name + '.pickle')















