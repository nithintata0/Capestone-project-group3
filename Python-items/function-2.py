from google.cloud import firestore
client = firestore.Client()
import requests
import os
# Python available modulses
import glob
import os
os.system("python -m spacy download en_core_web_sm")
import textract
from gensim.summarization.summarizer import summarize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import numpy as np
from os.path import isfile, join
from io import StringIO
from collections import Counter
import nltk
nltk.download('wordnet')
import en_core_web_sm
nlp = en_core_web_sm.load()
import spacy
#nlp = spacy.load('en_core_web_sm')
from spacy.matcher import PhraseMatcher
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


import re, string, unicodedata
import nltk
import inflect
from nltk import word_tokenize, sent_tokenize
#from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
from collections import Counter
import math
import tempfile
resume_list1=[]
# a=requests.get("https://firestore.googleapis.com/v1/projects/capestone-945f7/databases/(default)/documents/jobsApplied").json()
# for aa in a["documents"]:
#     resume_list1.append([aa["fields"]["url"]["stringValue"],aa["fields"]["resumeData"]["mapValue"]["fields"]["name"]["stringValue"].replace(" ","-")])

# to extract data

import re, string, unicodedata
import nltk
import inflect
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
from collections import Counter
import math


def remove_non_ascii(words):
    """Remove non-ASCII characters from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return new_words



def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words



def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words



def replace_numbers(words):
    """Replace all interger occurrences in list of tokenized words with textual representation"""
    p = inflect.engine()
    new_words = []
    for word in words:
        if word.isdigit():
            new_word = p.number_to_words(word)
            new_words.append(new_word)
        else:
            new_words.append(word)
    return new_words



def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    new_words = []
    for word in words:
        # print(word)
        if word not in stopwords.words('english'):
            new_words.append(word)
    return new_words



def stem_words(words):
    """Stem words in list of tokenized words"""
    stemmer = LancasterStemmer()
    stems = []
    for word in words:
        stem = stemmer.stem(word)
        stems.append(stem)
    return stems



def lemmatize_verbs(words):
    """Lemmatize verbs in list of tokenized words"""
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    for word in words:
        lemma = lemmatizer.lemmatize(word, pos='v')
        lemmas.append(lemma)
    return lemmas



def normalize(words):
    words = remove_non_ascii(words)
    words = to_lowercase(words)
    words = remove_punctuation(words)
    words = replace_numbers(words)
    #words = remove_stopwords(words)
    words = stem_words(words)
    words = lemmatize_verbs(words)
    return " ".join(words)
def extract_text_from_pdf(files_list):
    resumes = [] # Stores final processed resume files 
    for pdf_path in files_list:
        text = ''
        import tempfile
        pdf_path=os.path.join(tempfile.gettempdir(),"hello.pdf")
        print(pdf_path)
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
            resumes.append(normalize(text))
            
    df = {'Path':resume_list, 'File Name': resume_list[0].split('.')[0], 'Text':resumes, 'urls' : "hello.pdf"}
    #print(resume_list,file_names,resumes,resume_urls)
    data = pd.DataFrame(df)
    return data

#parsing job description

file_loc = '/Users/nithintata/Documents/GitHub/Capestone-project-group3/Original_Resumes/'
def parsing_jd(event):
#     path = file_loc + jd_file_name + '.txt'
#     for file in glob.glob(path, recursive=True):
#         if not file in job_desc_files: 
#             job_desc_files.append(file)
#     with open(path, 'rt') as file:
#         jd = file.read()
#     jd = summarize(jd, word_count=200)
#     file.close()
    jd=event["value"]["fields"]["jobDesc"]["stringValue"]
    jd = normalize(jd)  
    df = pd.DataFrame(columns=['Path', 'File Name', 'Text'])
    #df.loc[0] = [path, jd_file_name, jd]
    df.loc[0] = ['hello.pdf', 'hello', jd]
    return df


#calling function
def resume_df(files_list, jd_file_name, event):
    
    df1 = extract_text_from_pdf(files_list)
    df2 = parsing_jd(event)
    df3 = pd.concat([df1, df2], ignore_index = True)
    
    tfidfVect = TfidfVectorizer()
    tfidf = tfidfVect.fit_transform(df3['Text'])
    job_desc = df3[df3['File Name'] == 'hello']
    print(job_desc['Text'])
    print("----Na---")
    print(df3['Text'])
    
    jd_tfidfVect = TfidfVectorizer()
    jd_tfidfVect = jd_tfidfVect.fit(df3['Text'])
    jd_tfidf = jd_tfidfVect.transform(job_desc['Text'])
    
    nbrs = NearestNeighbors(n_neighbors=2).fit(tfidf)
    distances, indices = nbrs.kneighbors(jd_tfidf)
    names_similar = pd.Series(indices.flatten()).map(df3.reset_index()['File Name'])
    similar_urls = pd.Series(indices.flatten()).map(df3.reset_index()['urls'])
    result = pd.DataFrame({'Distance':distances.flatten(), 'Resume':names_similar, 'URLS' : similar_urls})
    print(result)
    print(result[1:2])
    return result[1:2]
    
fine_name=""
resume_list=[]
resume_urls=[]
def pre_process(event):
    global fine_name
    global resume_list
    #resume_list1=["https://firebasestorage.googleapis.com/v0/b/capestone-945f7.appspot.com/o/0q1yyOoSTOQKSJt1yDeh%2FNithin_Tataundefined?alt=media&token=66cdc9a4-0ce7-4dc2-b7ab-0c3040e9a8fa"]   
    resume_list1=[event["value"]['fields']["url"]['stringValue']]
    print(resume_list1)
    global resume_urls
    for i in resume_list1:
        resume_urls.append(i[0])
    #resume_list
    for file_url in zip(resume_list1,range(0,len(resume_list1))):
        response=requests.get(file_url[0])
        import tempfile
        fine_name=os.path.join(tempfile.gettempdir(),"hello.pdf")
        #fine_name=str("hello.pdf")
        print(fine_name)
        with open(fine_name, 'wb') as f:
            f.write(response.content)
        print("Cpmpleted")


    resume_list = [] # stores all resumes
    resume_list_pdf = [] # Captures files with pdf extension
    resume_list_doc = [] # Captures files with doc extension
    resume_list_docx = [] # Captures files with docx extension

    file_names = [] # STORES RESUME FILE NAMES
    job_desc_files = [] # stores jd paths

    for i in resume_list1:
        resume_list.append("hello.pdf")
    return resume_list                                   


def hello_firestore(event, context):
    print(event)
    print("na-1234")
    print(event["value"]["fields"]["jobDesc"]["stringValue"])
    print("na--123")
    print(event["value"]['fields']["url"]['stringValue'])
    
    pre= pre_process(event)                                     
    ss=resume_df(resume_list, 'sample',event)
    path_parts = context.resource.split('/documents/')[1].split('/')
    collection_path = path_parts[0]
    document_path = '/'.join(path_parts[1:])
    affected_doc = client.collection(collection_path).document(document_path)
    affected_doc.update({
            u'resumeValue':ss["Distance"].iloc[0]
        })