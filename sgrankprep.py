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


import textacy
import en_core_web_sm
import glob 
#import codecs
import csv

COMP_PATH = '../data/edison_competences/'
CV_PATH = '../data/CV/'
JOB_PATH = '../data/jobs/'


RES_BASE_PATH = '../results/'
RES_COMP_PATH = RES_BASE_PATH + 'sgrank/competences/'
RES_CV_PATH = RES_BASE_PATH + 'sgrank/CV/'
RES_JOB_PATH = RES_BASE_PATH + 'sgrank/jobs/'

TRANS_JOB_PATH = RES_BASE_PATH + 'jobs_en/jobs.jsonl'


def save_terms_csv(filePath, terms):
    with open(filePath, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for term in terms:
            writer.writerow([term[0].encode('utf-8'), term[1]])

def term_list(termScoreList):
    termList = []
    for term, _ in termScoreList:
        termList.append(term)
    return termList

def preprocess_edison_competences(in_path, out_path):
    import os
    spacy_lang = en_core_web_sm.load()
    for kag_path in glob.glob(in_path + '/*'):
        _ , kag_name = os.path.split(kag_path)
        for filename in glob.glob(kag_path + '/*.txt'):
            _ , comp_file = os.path.split(filename)
            if comp_file.index('.') >= 5:
                corpus = textacy.corpus.Corpus(spacy_lang)
                corpus.add_text(open(filename, 'r').read().decode('utf-8'))
#                doc_idf = corpus.word_doc_freqs(lemmatize=None, weighting='idf', lowercase=True, as_strings=True)
                termList = textacy.keyterms.sgrank(corpus[0], ngrams=(1, 2, 3), n_keyterms=30, normalize=u'lower', idf=None)
                res_file = '{}.csv'.format(comp_file[:-4]) 
                if not os.path.exists(out_path):
                    os.makedirs(out_path)
                save_terms_csv(out_path + res_file, termList)
#                break


def read_cv_corpus(cv_path):
    import json
    spacy_lang = en_core_web_sm.load()
    corpus = textacy.corpus.Corpus(spacy_lang)
    content = ''
    with open(cv_path) as cv_file:    
        content = json.load(cv_file)
    corpus_text = content.get('description', u'')
    corpus.add_text(corpus_text)
    return corpus

def preprocess_cvs(in_path, out_path):
    import os
    
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    for filename in glob.glob(in_path + '*.json'):
        _ , cv_file = os.path.split(filename)
        print(cv_file[:-5])
#        res_file = out_path + '{0}.csv'.format(cv_file[0:cv_file.index('.')])
        res_file = out_path + '{0}.csv'.format(cv_file[:-5])
        if not os.path.isfile(res_file):
            corpus = read_cv_corpus(filename)
            termList = textacy.keyterms.sgrank(corpus[0], ngrams=(1, 2, 3), n_keyterms=30, normalize=u'lower', idf=None)
            save_terms_csv(res_file, termList)


def preprocess_jobs(in_path, out_path):
    import os
    from pathlib import Path
    import json
    
    if not os.path.exists(out_path):
        os.makedirs(out_path)
        
    spacy_lang = en_core_web_sm.load()
    q = Path(in_path)
    with q.open() as f:
        for line in f:
            json_obj = json.loads(line.strip())
            try:
                corpus_text = json_obj["description"]
                jobid = json_obj['jobid']
            except:
                continue
            corpus = textacy.corpus.Corpus(spacy_lang)
            corpus.add_text(corpus_text)
            res_file = out_path + 'job{0}.csv'.format(jobid)
            termList = textacy.keyterms.sgrank(corpus[0], ngrams=(1, 2, 3), n_keyterms=30, normalize=u'lower', idf=None)
            save_terms_csv(res_file, termList)
    
    
if __name__ == '__main__':
#    preprocess_edison_competences(COMP_PATH,RES_COMP_PATH)
    preprocess_cvs(CV_PATH, RES_CV_PATH)
    preprocess_jobs(TRANS_JOB_PATH, RES_JOB_PATH)
