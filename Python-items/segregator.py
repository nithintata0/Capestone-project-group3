# Python available modules
import glob
import os
import textract
from gensim.summarization.summarizer import summarize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import numpy as np
from os.path import isfile, join
from io import StringIO
from collections import Counter

import spacy
nlp = spacy.load('en_core_web_sm')
from spacy.matcher import PhraseMatcher

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

# Developed Module
import text_process



resume_list = [] # stores all resumes
resume_list_pdf = [] # Captures files with pdf extension
resume_list_doc = [] # Captures files with doc extension
resume_list_docx = [] # Captures files with docx extension
 
file_names = [] # STORES RESUME FILE NAMES
job_desc_files = [] # stores jd paths

path = 'C:/Users/sampathi/PycharmProjects/Resume_Ranking/Automated-Resume-Ranking-System-master/Original_Resumes'
for file in glob.glob(path + '/*.pdf', recursive=True):
    resume_list_pdf.append(file)
for file in glob.glob('**/*.doc', recursive=True):
    resume_list_doc.append(file)
for file in glob.glob('**/*.docx', recursive=True):
    resume_list_docx.append(file)

resume_list = resume_list_doc + resume_list_docx + resume_list_pdf


def extract_text_from_pdf(files_list):
    resumes = [] # Stores final processed resume files 
    for pdf_path in files_list:
        text = ''
        with open(pdf_path, 'rb') as fh:
            # iterate over all pages of PDF document
            for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
                # creating a resoure manager
                resource_manager = PDFResourceManager()

                # create a file handle
                fake_file_handle = StringIO()

                # creating a text converter object
                converter = TextConverter(
                                    resource_manager, 
                                    fake_file_handle, 
                                    codec='utf-8', 
                                    laparams=LAParams()
                            )

                # creating a page interpreter
                page_interpreter = PDFPageInterpreter(
                                    resource_manager, 
                                    converter
                                )

                # process current page
                page_interpreter.process_page(page)

                # extract text
                text += fake_file_handle.getvalue()
                text = text.replace('\n', ' ')
                
                # close open handles
                converter.close()
                fake_file_handle.close()
            resumes.append(text_process.normalize(text))
            
    for name in resume_list:
        temp = name.split('.')[0]
        temp = temp.split('\\')[1]
        file_names.append(temp)
    df = {'Path':resume_list, 'File Name': file_names, 'Text':resumes}
    data = pd.DataFrame(df)
    return data



def resume_df(files_list, jd_file_name):
    
    df1 = extract_text_from_pdf(files_list)
    df2 = parsing_jd(jd_file_name)
    df3 = pd.concat([df1, df2], ignore_index = True)
    
    tfidfVect = TfidfVectorizer()
    tfidf = tfidfVect.fit_transform(df3['Text'])
    job_desc = df3[df3['File Name'] == jd_file_name]
    
    jd_tfidfVect = TfidfVectorizer()
    jd_tfidfVect = jd_tfidfVect.fit(df3['Text'])
    jd_tfidf = jd_tfidfVect.transform(job_desc['Text'])
    
#     feature_array = np.array(feature_names)
#     tfidf_sorting = np.argsort(jd_tfidf.toarray()).flatten()[::-1]
#     top_n = feature_array[tfidf_sorting][:10]
    
    nbrs = NearestNeighbors(n_neighbors=5).fit(tfidf)
    distances, indices = nbrs.kneighbors(jd_tfidf)
    names_similar = pd.Series(indices.flatten()).map(df3.reset_index()['File Name'])
    result = pd.DataFrame({'Distance':distances.flatten(), 'Resume':names_similar})
    
    return result[1:]


    resume_df(resume_list, 'sample1').head()

