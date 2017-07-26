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

from pathlib import Path
import textacy

BASE_PATH = '/../results/'
COMP_PATH = '/../data/competences_manual/'
JOB_PATH = BASE_PATH + 'sgrank/jobs'
CV_PATH = BASE_PATH + 'sgrank/CV/'

RES_JOBCOMP_PATH = BASE_PATH + 'jaccard/jobcomp/'
RES_CVCOMP_PATH = BASE_PATH + 'jaccard/cvcomp/'
RES_JOBCV_PATH = BASE_PATH + 'jaccard/jobcv/'

### Using keyterms instead of whole job ad
def get_terms(filepath):
    term_list = []
    with open(filepath, 'r') as jf: 
        content = jf.readlines()
        for line in content:
            tokens = line.split(',')
            term_list.append(tokens[0])
    return term_list

def jaccard_jobcomp():
    import os
    res_path = os.getcwd() + RES_JOBCOMP_PATH
    if not os.path.exists(res_path):
        os.makedirs(res_path)
    res_file_path = res_path + "jobcomp.csv"
    res_file = Path(res_file_path)
    if res_file.is_file():
        os.remove(res_file_path)
    jobpath = os.getcwd() + JOB_PATH
    comppath = os.getcwd() + COMP_PATH
    job_count = 0
    for jobfile in os.listdir(jobpath):
#        if jobfile[-3:] == "csv" and job_count < 100:
        _ , job_file = os.path.split(jobfile)
        jobterms = get_terms(jobpath + '/' + jobfile)
        comp_count = 0
        for compfile in os.listdir(comppath):
            _ , comp_file = os.path.split(compfile)
            if compfile[-3:] == "csv":
                try:
                    fullpath = comppath + '/' + compfile
                    compterms = get_terms(fullpath)
                    jc_sim = textacy.similarity.jaccard(jobterms, compterms, fuzzy_match = True)
                    with open(res_file_path, mode="a") as text_file:
                       text_file.write(str(job_count) + "," + str(comp_count) + "," + compfile[:-4] + "," + str(jc_sim) + "\n")
                    comp_count += 1
                except:
                    print(fullpath)
                    continue
        job_count += 1



def jaccard_cvcomp():
    import os
    res_path = os.getcwd() + RES_CVCOMP_PATH
    if not os.path.exists(res_path):
        os.makedirs(res_path)
    res_file_path = res_path + "cvcomp.csv"
    res_file = Path(res_file_path)
    if res_file.is_file():
        os.remove(res_file_path)
    cvpath = os.getcwd() + CV_PATH
    comppath = os.getcwd() + COMP_PATH
    cv_count = 0
    for cvfile in os.listdir(cvpath):
        if cvfile[-3:] == "csv":
            _ , cv_file = os.path.split(cvfile)
            cvterms = get_terms(cvpath + '/' + cvfile)
            comp_count = 0
            for compfile in os.listdir(comppath):
                _ , comp_file = os.path.split(compfile)
                if compfile[-3:] == "csv":
                    try:
                        fullpath = comppath + '/' + compfile
                        compterms = get_terms(fullpath)
                        cc_sim = textacy.similarity.jaccard(cvterms, compterms, fuzzy_match = True)
                        with open(res_file_path, mode="a") as text_file:
                           text_file.write(str(cv_count) + "," + str(comp_count) + "," + compfile[:-4] + "," + str(cc_sim) + "\n")
                        comp_count += 1
                    except:
                        print(fullpath)
                        continue
            cv_count += 1


def jaccard_jobcv():
    import os
    res_path = os.getcwd() + RES_JOBCV_PATH
    if not os.path.exists(res_path):
        os.makedirs(res_path)
    res_file_path = res_path + "jobcv.csv"
    res_file = Path(res_file_path)
    if res_file.is_file():
        os.remove(res_file_path)
    jobpath = os.getcwd() + JOB_PATH
    cvpath = os.getcwd() + CV_PATH
    job_count = 0
    for jobfile in os.listdir(jobpath):
        if jobfile[-3:] == "csv":
            _ , job_file = os.path.split(jobfile)
            jobterms = get_terms(jobpath + '/' + jobfile)
            cv_count = 0
            for cvfile in os.listdir(cvpath):
                _ , cv_file = os.path.split(cvfile)
                if cvfile[-3:] == "csv":
                    try:
                        fullpath = cvpath + '/' + cvfile
                        cvterms = get_terms(fullpath)
                        jc_sim = textacy.similarity.jaccard(jobterms, cvterms, fuzzy_match = True)
                        with open(res_file_path, mode="a") as text_file:
                           text_file.write(str(job_count) + "," + str(cv_count) + "," + str(jc_sim) + "\n")
                        cv_count += 1
                    except:
                        print(fullpath)
                        continue
            job_count += 1



if __name__ == '__main__':
    jaccard_jobcomp()
    jaccard_cvcomp()
    jaccard_jobcv()
