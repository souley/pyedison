# -*- coding: utf-8 -*-
"""
/*
 * Copyright 2017 Instituut voor Informatica, Universiteit van Amsterdam.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */"""


import glob 
import codecs

BASE_PATH = '../results/'
COMP_PATH = BASE_PATH + 'sgrank/competences_manual/'
JOB_PATH = BASE_PATH + 'sgrank/jobs'
CV_PATH = BASE_PATH + 'sgrank/CV/'
#COMP_PATH = '../data/edison_competences/'
#CV_PATH = '../data/CV/'
#JOB_PATH = '../data/jobs/data1apriltest.docx'


#TRANS_JOB_PATH = RES_BASE_PATH + 'jobs_en/jobs.jsonl'
#RES_COMP_PATH = RES_BASE_PATH + 'sgrank/competences/'
#RES_CV_PATH = RES_BASE_PATH + 'sgrank/CV/'
#RES_JOB_PATH = RES_BASE_PATH + 'sgrank/jobs/'

from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models, similarities
import os

from pathlib import Path


def clean_text(text):
    from nltk.corpus import stopwords 
#    from nltk.stem.wordnet import WordNetLemmatizer
    import string
    tokenizer = RegexpTokenizer(r'\w+')
    p_stemmer = PorterStemmer()
    
    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation) 

    raw = text.lower()#.decode('utf-8', 'ignore')
    tokens = tokenizer.tokenize(raw)
    
    # remove stop words from tokens
    stopped_tokens = [i for i in tokens if not i in stop]
    
    punc_free = [ch for ch in stopped_tokens if ch not in exclude]
    
    stemmed_tokens = [p_stemmer.stem(i) for i in punc_free]
#        stemmed_tokens = [WordNetLemmatizer().lemmatize(word) for word in stopped_tokens]
    # add tokens to list
    return stemmed_tokens
        
    


def clean(filepath, tjson=None):
    import json
    with codecs.open(filepath, 'r', encoding='utf-8') as rfile:
        if not tjson is None:
            content = json.load(rfile)
            content = content.get('description', u'')
        else:
            content = rfile.read()
        
        return clean_text(content)

### Dictionary of dictionaries, each holding SGrank scores of its terms
doc_term_scores = {}

def prep_ngrams(term):
    tokens = term.split(' ')
    if len(tokens) >= 2:
        return '_'.join(token for token in tokens)
    return tokens[0]

def get_comp_vocab(comp_path, comp_name):
    import csv
    terms = []
    if not comp_name in doc_term_scores:
        doc_term_scores[comp_name] = {}
    with open(comp_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            keyterm = prep_ngrams(row[0])
            terms.append(keyterm.encode('utf-8'))
            doc_term_scores[comp_name][keyterm] =  float(row[1])
    return terms


def read_comp_corpus():
    texts = {}
    for comp_path in glob.glob(COMP_PATH + '/*.csv'):
        _ , comp_file = os.path.split(comp_path)
        comp_key = comp_file[:-4]
        print(comp_key)
        texts[comp_key] = get_comp_vocab(comp_path, comp_key)
    return texts

def get_vocab(job_path):
    import csv
    terms = []
    with open(job_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            keyterm = prep_ngrams(row[0])
#            keyterm = keyterm.encode('ascii', 'ignore')
            terms.append(keyterm)
    return terms

def get_rank(term, doc):
    if term in doc_term_scores[doc]:
        return doc_term_scores[doc][term]
    else:
        return 0.0


def no_idf(df,nb):
    return 1.0


def job_comp_sims():
    texts = read_comp_corpus()
    print(texts.values())
    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(texts.values())
        
    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in texts.values()]
    
    # Transform Text with TF-IDF
#    tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model
    tfidf = models.TfidfModel(corpus, wglobal=no_idf) 
#    tfidf = models.TfidfModel(corpus, wlocal=get_rank, wglobal=no_idf) # step 1 -- initialize a model

    res_path = os.getcwd() + '/../results/sgrank/jobcomp/'
    if not os.path.exists(res_path):
        os.makedirs(res_path)
    res_file_path = res_path + "jobcomp.csv"
    res_file = Path(res_file_path)
    if res_file.is_file():
        os.remove(res_file_path)
    job_count = 0
    
    for job_path in glob.glob(JOB_PATH + '/*.csv'):
        job_text = get_vocab(job_path)
        job_bow = dictionary.doc2bow(job_text)
        job_tfidf = tfidf[job_bow]
        index = similarities.MatrixSimilarity(tfidf[corpus])
        sims = index[job_tfidf]
        comps = texts.keys()
        comp_count = 0
        print('###Writing sims for job '+str(job_count))
        with open(res_file_path, mode="a") as text_file:
            for doc,sim in enumerate(sims):
                text_file.write(str(job_count) + "," + str(comp_count) + "," + comps[doc] + "," + str(sim) + "\n")
                comp_count += 1           
        job_count += 1

def cv_comp_sims():
    texts = read_comp_corpus()
    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(texts.values())
        
    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in texts.values()]
    
    # Transform Text with TF-IDF
    tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model

    ## compute similarities for CVs 
    res_path = os.getcwd() + '/../results/sgrank/cvcomp/'
    if not os.path.exists(res_path):
        os.makedirs(res_path)
    res_file_path = res_path + "cvcomp.csv"
    res_file = Path(res_file_path)
    if res_file.is_file():
        os.remove(res_file_path)
    cv_count = 0
    for filename in glob.glob(CV_PATH + '*.csv'):
#        cv_text = clean(filename, 'json')
        cv_text = get_vocab(filename)
        cv_bow = dictionary.doc2bow(cv_text)
        cv_tfidf = tfidf[cv_bow]
        index = similarities.MatrixSimilarity(tfidf[corpus])
        sims = index[cv_tfidf]
        comps = texts.keys()
        comp_count = 0
        with open(res_file_path, mode="a") as text_file:
            for doc,sim in enumerate(sims):
                text_file.write(str(cv_count) + "," + str(comp_count) + "," + comps[doc] + "," + str(sim) + "\n")
                comp_count += 1           
        cv_count += 1


def read_job_corpus():
    texts = {}
    for job_path in glob.glob(JOB_PATH + '/*.csv'):
        _ , job_file = os.path.split(job_path)
        job_key = job_file[:-4]
        texts[job_key] = get_vocab(job_path)
    return texts

def job_cv_sims():
    texts = read_job_corpus()
    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(texts.values())
        
    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in texts.values()]
    
    # Transform Text with TF-IDF
    tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model

    res_path = os.getcwd() + '/../results/sgrank/jobcv/'
    if not os.path.exists(res_path):
        os.makedirs(res_path)
    res_file_path = res_path + "jobcv.csv"
    res_file = Path(res_file_path)
    if res_file.is_file():
        os.remove(res_file_path)
    ## compute similarities for CVs 
    cv_count = 0
    for filename in glob.glob(CV_PATH + '*.csv'):
#        cv_text = clean(filename, 'json')
        cv_text = get_vocab(filename)
        cv_bow = dictionary.doc2bow(cv_text)
        cv_tfidf = tfidf[cv_bow]
        index = similarities.MatrixSimilarity(tfidf[corpus])
        sims = index[cv_tfidf]
        comp_count = 0
        with open(res_file_path, mode="a") as text_file:
            for doc,sim in enumerate(sims):
                text_file.write(str(cv_count) + "," + str(doc) + "," + str(sim) + "\n")
                comp_count += 1           
        cv_count += 1         

if __name__ == '__main__':
    job_comp_sims()
    cv_comp_sims()
    job_cv_sims()
