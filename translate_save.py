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
 */
"""

JOB_PATH = '../data/jobs/data1apriltest.docx'
RES_BASE_PATH = '/../results/'
TRANS_JOB_PATH = RES_BASE_PATH + 'jobs_en/'

import os

def save_translated_job(file_path, id, text):
    import json
    jeysan = {}
    jeysan['jobid'] = id
    jeysan['description'] = text.replace('\n', ' ')    
    with open(file_path, mode="a") as text_file:
        text_file.write(json.dumps(jeysan, ensure_ascii=False) + u"\n")

def translate_and_save_jobs():
    res_path = os.getcwd() + TRANS_JOB_PATH
    if not os.path.exists(res_path):
        os.makedirs(res_path)
    elif os.listdir(res_path):
        return
    job_count = 0
    from docx import Document
    from googletrans import Translator
    wordDoc = Document(JOB_PATH)
    job_count = 0
    for table in wordDoc.tables:
        desc = ''
        req = ''
        for row in table.rows:
            for cell in row.cells:
                if cell.text == "Functieomschrijving":
                    desc = row.cells[1].text
                if cell.text == "Functie-eisen":
                    req = row.cells[1].text
        if desc and req:
            job_text_nl = '\n'.join(text for text in [desc, req])
            translator = Translator()
            job_text = translator.translate(job_text_nl, dest='en').text
            job_text = job_text.encode('ascii', 'ignore')
            job_text = job_text.decode('utf-8')
            save_translated_job(res_path + 'jobs.jsonl', job_count, job_text)
            job_count += 1


if __name__ == '__main__':
    translate_and_save_jobs()
