# Python available modules
import glob
import os
from typing import AsyncContextManager
from gensim.summarization.summarizer import summarize
import pandas as pd
import numpy as np
from os.path import isfile, join
from io import StringIO
from collections import Counter
import nltk
nltk.download('wordnet')
print("Download completed")
# import spacy
# nlp = spacy.load('en_core_web_sm')
# from spacy.matcher import PhraseMatcher
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
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

path = '/Users/nithintata/Documents/GitHub/Capestone-project-group3/Original_Resumes'
file_loc = '/Users/nithintata/Documents/GitHub/Capestone-project-group3/Original_Resumes/'
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
        #print(name)
        temp = name.split('.')[0]
        temp = temp.split('/')[1]
        file_names.append(temp)
    df = {'Path':resume_list, 'File Name': file_names, 'Text':resumes}
    data = pd.DataFrame(df)
    data.to_csv('out.csv')
    return data

re_data = extract_text_from_pdf(resume_list)

def parsing_jd(jd_file_name):
    path = file_loc + jd_file_name + '.rtf'
    for file in glob.glob(path, recursive=True):
        if not file in job_desc_files: 
            job_desc_files.append(file)
    with open(path, 'rt') as file:
        jd = file.read()
    jd = summarize(jd, word_count=200)
    file.close()
    jd = text_process.normalize(jd)
    
#     dict = {'Path':path, 'File Name': jd_file_name, 'Text':jd}
#     df = pd.DataFrame(dict)
    
    df = pd.DataFrame(columns=['Path', 'File Name', 'Text'])
    df.loc[0] = [path, jd_file_name, jd]
    return df

def resume_df(files_list, jd_file_name):
    
    df1 = extract_text_from_pdf(files_list)
    print("DF1",df1)
    df2 = parsing_jd(jd_file_name)
    print("DF2",df2)
    df3 = pd.concat([df1, df2], ignore_index = True)
    
    tfidfVect = TfidfVectorizer()
    print(df3['Text'])
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

print(resume_df(resume_list, 'sample').head())

