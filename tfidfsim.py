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

COMP_PATH = '../data/edison_prep_competences2/'
CV_PATH = '../data/CV/'
JOB_PATH = '../data/jobs/data1apriltest.docx'

RES_BASE_PATH = '../results/'
TRANS_JOB_PATH = RES_BASE_PATH + 'jobs_en/jobs.jsonl'
RES_COMP_PATH = RES_BASE_PATH + 'sgrank/competences/'
RES_CV_PATH = RES_BASE_PATH + 'sgrank/CV/'
RES_JOB_PATH = RES_BASE_PATH + 'sgrank/jobs/'

CV_KEYTERM_PATH = RES_BASE_PATH + 'sgrank/CV/'

ORDERED_COMPS = ['DSDA', 'DSENG', 'DSDM', 'DSRM', 'DSDK']

from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models, similarities
import os

from pathlib import Path

STEM_OUT = ['includ', 'non', 'common', 'direct', 'type', 'particular', 'focu', 'data', 'q', 'g', 'script', 'system',
            'wide', 'modern', 'need', 'activ', 'public', 'result', 'key', 'valid', 'etc', 'whole', 'effect', 
            'driven', 'avail', 'similar', 'ap', 'other', 'e']

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

    stemmed_tokens = [stem for stem in stemmed_tokens if stem not in STEM_OUT]
    # add tokens to list
    return stemmed_tokens
        
    


def clean(filepath, tjson=None, raw=False):
    import json
    with codecs.open(filepath, 'r', encoding='utf-8') as rfile:
        if not tjson is None:
            content = json.load(rfile)
            content = content.get('description', u'')
        else:
            content = rfile.read()
        if raw:
            return content
        return clean_text(content)


def read_comp_doc():
    import collections
    texts = collections.OrderedDict()
#    texts = {}
    ORDERED_COMPS
#    for kag_path in glob.glob(COMP_PATH + '/*'):
#        _ , kag_name = os.path.split(kag_path)
    for kag_name in ORDERED_COMPS:
        kag_path = COMP_PATH + '/' + kag_name
#        print(kag_name)
        for comp_path in glob.glob(kag_path + '/*.txt'):
            _ , comp_file = os.path.split(comp_path)
            comp_key = comp_file[:-4]
            texts[comp_key] = clean(comp_path)
    return texts

#def save_translated_job(file_path, id, text):
#    import json
#    jeysan = {}
#    jeysan['jobid'] = id
#    jeysan['description'] = text.replace('\n', ' ')    
#    with open(file_path, mode="a") as text_file:
#        text_file.write(json.dumps(jeysan, ensure_ascii=False) + u"\n")
#
#def translate_and_save_jobs():
#    res_path = os.getcwd() + TRANS_JOB_PATH
#    if not os.path.exists(res_path):
#        os.makedirs(res_path)
#    job_count = 0
#    from docx import Document
#    from googletrans import Translator
#    wordDoc = Document(JOB_PATH)
#    job_count = 0
#    for table in wordDoc.tables:
#        desc = ''
#        req = ''
#        for row in table.rows:
#            for cell in row.cells:
#                if cell.text == "Functieomschrijving":
#                    desc = row.cells[1].text
#                if cell.text == "Functie-eisen":
#                    req = row.cells[1].text
#        if desc and req:
#            job_text_nl = '\n'.join(text for text in [desc, req])
#            translator = Translator()
#            job_text = translator.translate(job_text_nl, dest='en').text
#            job_text = job_text.encode('ascii', 'ignore')
#            job_text = job_text.decode('utf-8')
#            save_translated_job(TRANS_JOB_PATH, job_count, job_text)
#            job_count += 1


def convert(types, values):
    return [t(v) for t, v in zip(types, values)]
  
def job_comp_sims():
    import json
    import csv
    import operator
    texts = read_comp_doc()
    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(texts.values())
    print('===DICTIONARY===')
#    print(str(type(dictionary)))
    print ' '.join(p for p in dictionary.values()) 
    print('===END DICTIONARY===')
    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in texts.values()]
    
    # Transform Text with TF-IDF
    tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model
    
    res_path = os.getcwd() + '/../results/tfidf/jobcomp/'
    if not os.path.exists(res_path):
        os.makedirs(res_path)
    res_file_path = res_path + "jobcomp.csv"
    res_file = Path(res_file_path)
    if res_file.is_file():
        os.remove(res_file_path)
    jc_sims = []
    q = Path(TRANS_JOB_PATH)
    with q.open() as f:
        for line in f:
            json_obj = json.loads(line.strip())
            try:
                job_text = json_obj["description"]
                job_count = int(json_obj['jobid'])
            except:
                continue
            job_text = clean_text(job_text)
            job_bow = dictionary.doc2bow(job_text)
            job_tfidf = tfidf[job_bow]
            index = similarities.MatrixSimilarity(tfidf[corpus])
            sims = index[job_tfidf]
            comps = texts.keys()
            comp_count = 0
#            print('###Writing sims for job '+str(job_count))
#            with open(res_file_path, mode="a") as text_file:
            for doc,sim in enumerate(sims):
                jc_sims.append(convert((int, int, str, float), (job_count, comp_count, comps[doc], sim)))
#                    text_file.write(str(job_count) + "," + str(comp_count) + "," + comps[doc] + "," + str(sim) + "\n")
                comp_count += 1           
#            job_count += 1
#    jc_sims.sort(key=operator.itemgetter(*(0,3)))
    with open(res_file_path, mode="a") as text_file:
        csv.writer(text_file).writerows(jc_sims)

def prep_ngrams(term):
    tokens = term.split(' ')
    if len(tokens) >= 2:
        return '_'.join(token for token in tokens)
    return tokens[0]

def preprocess_cv(cvname, cvtext):
    import csv
    cv_path = CV_KEYTERM_PATH + cvname + 'csv'
    prep_text = cvtext
    with open(cv_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            keyterm = prep_ngrams(row[0])
            prep_text = prep_text.encode('ascii', 'ignore').replace(row[0], keyterm)
#    print(prep_text)
    return prep_text

def cv_comp_sims():
    import csv
    import operator
    texts = read_comp_doc()
    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(texts.values())
    
    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in texts.values()]
    
    # Transform Text with TF-IDF
    tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model

    ## compute similarities for CVs 
    res_path = os.getcwd() + '/../results/tfidf/cvcomp/'
    if not os.path.exists(res_path):
        os.makedirs(res_path)
    res_file_path = res_path + "cvcomp.csv"
    res_file = Path(res_file_path)
    if res_file.is_file():
        os.remove(res_file_path)
    cv_count = 0
    cc_sims = []
    for filename in glob.glob(CV_PATH + '*.json'):
        _ , cv_name = os.path.split(filename)
        cv_text = clean(filename, 'json', raw=True)
        prep_text = preprocess_cv(cv_name[:-4], cv_text)
        clprep_text = clean_text(prep_text)
        cv_bow = dictionary.doc2bow(clprep_text)
        cv_tfidf = tfidf[cv_bow]
        index = similarities.MatrixSimilarity(tfidf[corpus])
        sims = index[cv_tfidf]
        comps = texts.keys()
        comp_count = 0
#        with open(res_file_path, mode="a") as text_file:
        for doc,sim in enumerate(sims):
            cc_sims.append(convert((int, int, str, float), (cv_count, comp_count, comps[doc], sim)))
#                text_file.write(str(cv_count) + "," + str(comp_count) + "," + comps[doc] + "," + str(sim) + "\n")
            comp_count += 1           
        cv_count += 1
#    cc_sims.sort(key=operator.itemgetter(*(0,3)))
    with open(res_file_path, mode="a") as text_file:
        csv.writer(text_file).writerows(cc_sims)


def read_job_doc():
    import json
    texts = {}
    q = Path(TRANS_JOB_PATH)
    with q.open() as f:
        for line in f:
            json_obj = json.loads(line.strip())
            try:
                job_text = json_obj["description"]
                job_count = int(json_obj['jobid'])
            except:
                continue
            texts[job_count] = clean_text(job_text)
#            job_count += 1
    return texts


def job_cv_sims():
    import csv
    import operator
    texts = read_job_doc()
    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(texts.values())
        
    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in texts.values()]
    
    # Transform Text with TF-IDF
    tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model

    res_path = os.getcwd() + '/../results/tfidf/jobcv/'
    if not os.path.exists(res_path):
        os.makedirs(res_path)
    res_file_path = res_path + "jobcv.csv"
    res_file = Path(res_file_path)
    if res_file.is_file():
        os.remove(res_file_path)
    ## compute similarities for CVs 
    cv_count = 0
    jc_sims = []
    for filename in glob.glob(CV_PATH + '*.json'):
        cv_text = clean(filename, 'json')
        cv_bow = dictionary.doc2bow(cv_text)
        cv_tfidf = tfidf[cv_bow]
        index = similarities.MatrixSimilarity(tfidf[corpus])
        sims = index[cv_tfidf]
        comp_count = 0
#        with open(res_file_path, mode="a") as text_file:
        for doc,sim in enumerate(sims):
            jc_sims.append(convert((int, int, float), (cv_count, comp_count, sim)))
#                text_file.write(str(cv_count) + "," + str(doc) + "," + str(sim) + "\n")
            comp_count += 1           
        cv_count += 1         
    jc_sims.sort(key=operator.itemgetter(*(0,2)))
    with open(res_file_path, mode="a") as text_file:
        csv.writer(text_file).writerows(jc_sims)

if __name__ == '__main__':
#    translate_and_save_jobs()
    job_comp_sims()
    cv_comp_sims()
    job_cv_sims()
