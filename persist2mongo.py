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

#Script that writes things to a running mongodb
from pymongo import MongoClient
import os
from pathlib import Path
import json

def tfidf_cvcomp_collection(db):
    collection = db['tfidf_cvcomp']
    path = '../results/tfidf/cvcomp'
    for filename in os.listdir(path):
        if filename[-3:] == "csv":
            fullpath = path + '/' + filename
            q = Path(fullpath)
            with q.open() as f:
                for line in f:
                    # "cvid", "cpid", "category", "distance"
                    cvid, cpid, category, distance = line.strip().split(',')
                    obj = {"cvid": int(cvid), "cpid": int(cpid), \
                    "category": category, "distance": float(distance)}
                    collection.insert_one(obj)



def tfidf_jobcomp_collection(db):
    collection = db['tfidf_jobcomp']
    path = '../results/tfidf/jobcomp'
    for filename in os.listdir(path):
        if filename[-3:] == "csv":
            fullpath = path + '/' + filename
            q = Path(fullpath)
            with q.open() as f:
                for line in f:
                    # "jobid", "cpid", "category", "distance"
                    jobid, cpid, category, distance = line.strip().split(',')
                    obj = {"jobid": int(jobid), "cpid": int(cpid), \
                    "category": category, "distance": float(distance)}
                    collection.insert_one(obj)


def tfidf_jobcv_collection(db):
    collection = db['tfidf_jobcv']
    path = '../results/tfidf/jobcv'
    for filename in os.listdir(path):
        if filename[-3:] == "csv":
            fullpath = path + '/' + filename
            q = Path(fullpath)
            with q.open() as f:
                for line in f:
                    #"jobid", "jobid", "distance"
                    cvid, jobid, distance = line.strip().split(',')
                    obj = {"cvid": int(cvid), "jobid": int(jobid), "distance": float(distance)}
                    collection.insert_one(obj)


def persist_raw_cvs(db):
    import codecs
    collection = db['raw_cvs']
    path = os.getcwd() + '/../data/CV'
    for filename in os.listdir(path):
        if filename[-4:] == "json":
            try:
                fullpath = path + '/' + filename
                with codecs.open(fullpath) as cv_file:    
                    content = json.load(cv_file)
                    obj = {"cvid": content['cvid'], "description": content["description"]}
                    collection.insert_one(obj)
            except:
                print(fullpath)
                continue


def persist_raw_jobs(db):
    collection = db['raw_jobs']
    q = Path('../results/jobs_en/jobs.jsonl')
    with q.open() as f:
        for line in f:
            json_obj = json.loads(line.strip())
            try:
                obj = {"jobid": json_obj['jobid'], "description": json_obj["description"]}
                collection.insert_one(obj)
            except:
                continue

def sgrank_cvcomp_collection(db):
    collection = db['sgrank_cvcomp']
    path = '../results/sgrank/cvcomp'
    for filename in os.listdir(path):
        if filename[-3:] == "csv":
            fullpath = path + '/' + filename
            q = Path(fullpath)
            with q.open() as f:
                for line in f:
                    # "cvid", "cpid", "category", "distance"
                    cvid, cpid, category, distance = line.strip().split(',')
                    obj = {"cvid": int(cvid), "cpid": int(cpid), \
                    "category": category, "distance": float(distance)}
                    collection.insert_one(obj)



def sgrank_jobcomp_collection(db):
    collection = db['sgrank_jobcomp']
    path = '../results/sgrank/jobcomp'
    for filename in os.listdir(path):
        if filename[-3:] == "csv":
            fullpath = path + '/' + filename
            q = Path(fullpath)
            with q.open() as f:
                for line in f:
                    # "jobid", "cpid", "category", "distance"
                    jobid, cpid, category, distance = line.strip().split(',')
                    obj = {"jobid": int(jobid), "cpid": int(cpid), \
                    "category": category, "distance": float(distance)}
                    collection.insert_one(obj)


def sgrank_jobcv_collection(db):
    collection = db['sgrank_jobcv']
    path = '../results/sgrank/jobcv'
    for filename in os.listdir(path):
        if filename[-3:] == "csv":
            fullpath = path + '/' + filename
            q = Path(fullpath)
            with q.open() as f:
                for line in f:
                    #"jobid", "jobid", "distance"
                    cvid, jobid, distance = line.strip().split(',')
                    obj = {"cvid": int(cvid), "jobid": int(jobid), "distance": float(distance)}
                    collection.insert_one(obj)


def jaccard_cvcomp_collection(db):
    collection = db['jacc_cvcomp']
    path = '../results/jaccard/cvcomp'
    for filename in os.listdir(path):
        if filename[-3:] == "csv":
            fullpath = path + '/' + filename
            q = Path(fullpath)
            with q.open() as f:
                for line in f:
                    # "cvid", "cpid", "category", "distance"
                    cvid, cpid, category, distance = line.strip().split(',')
                    obj = {"cvid": int(cvid), "cpid": int(cpid), \
                    "category": category, "distance": float(distance)}
                    collection.insert_one(obj)



def jaccard_jobcomp_collection(db):
    collection = db['jacc_jobcomp']
    path = '../results/jaccard/jobcomp'
    for filename in os.listdir(path):
        if filename[-3:] == "csv":
            fullpath = path + '/' + filename
            q = Path(fullpath)
            with q.open() as f:
                for line in f:
                    # "jobid", "cpid", "category", "distance"
                    jobid, cpid, category, distance = line.strip().split(',')
                    obj = {"jobid": int(jobid), "cpid": int(cpid), \
                    "category": category, "distance": float(distance)}
                    collection.insert_one(obj)


def jaccard_jobcv_collection(db):
    collection = db['jacc_jobcv']
    path = '../results/jaccard/jobcv'
    for filename in os.listdir(path):
        if filename[-3:] == "csv":
            fullpath = path + '/' + filename
            q = Path(fullpath)
            with q.open() as f:
                for line in f:
                    #"jobid", "jobid", "distance"
                    jobid, cvid, distance = line.strip().split(',')
                    obj = {"jobid": int(jobid), "cvid": int(cvid), "distance": float(distance)}
                    collection.insert_one(obj)


def lda_cvcomp_collection(db):
    collection = db['lda_cvcomp']
    path = '../results/lda/cvcomp'
    for filename in os.listdir(path):
        if filename[-3:] == "csv":
            fullpath = path + '/' + filename
            q = Path(fullpath)
            with q.open() as f:
                for line in f:
                    # "cvid", "cpid", "category", "distance"
                    cvid, cpid, category, distance = line.strip().split(',')
                    obj = {"cvid": int(cvid), "cpid": int(cpid), \
                    "category": category, "distance": float(distance)}
                    collection.insert_one(obj)



def lda_jobcomp_collection(db):
    collection = db['lda_jobcomp']
    path = '../results/lda/jobcomp'
    for filename in os.listdir(path):
        if filename[-3:] == "csv":
            fullpath = path + '/' + filename
            q = Path(fullpath)
            with q.open() as f:
                for line in f:
                    # "jobid", "cpid", "category", "distance"
                    jobid, cpid, category, distance = line.strip().split(',')
                    obj = {"jobid": int(jobid), "cpid": int(cpid), \
                    "category": category, "distance": float(distance)}
                    collection.insert_one(obj)


def lda_jobcv_collection(db):
    collection = db['lda_jobcv']
    path = '../results/lda/jobcv'
    for filename in os.listdir(path):
        if filename[-3:] == "csv":
            fullpath = path + '/' + filename
            q = Path(fullpath)
            with q.open() as f:
                for line in f:
                    #"jobid", "jobid", "distance"
                    cvid, jobid, distance = line.strip().split(',')
                    obj = {"cvid": int(cvid), "jobid": int(jobid), "distance": float(distance)}
                    collection.insert_one(obj)


def main():
    client = MongoClient('localhost', 27017)
    db = client['erwin2']

    persist_raw_cvs(db)
    persist_raw_jobs(db)

    tfidf_jobcomp_collection(db)
    tfidf_cvcomp_collection(db) 
    tfidf_jobcv_collection(db)

#    sgrank_jobcomp_collection(db)
#    sgrank_cvcomp_collection(db) 
#    sgrank_jobcv_collection(db)

    lda_jobcomp_collection(db)
    lda_cvcomp_collection(db) 
    lda_jobcv_collection(db)

    jaccard_jobcomp_collection(db)
    jaccard_cvcomp_collection(db) 
    jaccard_jobcv_collection(db)
    


if __name__ == '__main__':
    main()

