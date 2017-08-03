from nltk.tokenize import RegexpTokenizer
#from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models, similarities
#import gensim
from gensim.models.coherencemodel import CoherenceModel
import pyLDAvis.gensim

import glob
import os

from pathlib import Path

#KAG_BASE_PATH = '../data/Competences/'
#RES_BASE_PATH = '../results/'
#JOB_PATH = '../data/jobs_json/'
#NEWJOB_PATH = '../data/newjobs_json/'
CV_PATH = '../data/CV/'
#COMP2_BASE_PATH = '../data/raw_competence2/'
COMP_PATH = '../data/edison_prep_competences/'
JOB_PATH = '../results/jobs_en/jobs.jsonl'

tokenizer = RegexpTokenizer(r'\w+')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()
    

def clean_text(text):
    from nltk.corpus import stopwords 
#    from nltk.stem.wordnet import WordNetLemmatizer
    import string
    stop = set(stopwords.words('english'))
    
    exclude = set(string.punctuation) 
#    lemma = WordNetLemmatizer()
        
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
    import codecs
    with codecs.open(filepath, 'r', encoding='utf-8') as rfile:
        if not tjson is None:
            content = json.load(rfile)
            content = content.get('description', u'')
        else:
            content = rfile.read()
        return clean_text(content)


def read_comp_doc():
    texts = {}
    for comp_path in glob.glob(COMP_PATH + '/*'):
        print('=comp_path: ' + comp_path)
        for filename in glob.glob(comp_path + '/*.txt'):
            _ , comp_file = os.path.split(filename)
            comp_name = comp_file[:-4]
            print('=competence: ' + comp_name)
            texts[comp_name] = clean(filename) #tokenize_clean(filename)
    return texts

def job_comp_sims():
    import json
    texts = read_comp_doc()
    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(texts.values())
        
    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in texts.values()]
    
    # generate LDA model
    ldamodel = models.ldamodel.LdaModel(corpus, num_topics=40, id2word = dictionary, passes=50)
    #print(ldamodel.print_topics(num_topics=5))
    cm = CoherenceModel(model=ldamodel, texts=texts.values(), dictionary=dictionary, coherence='c_v')
    print(cm.get_coherence())

    res_path = os.getcwd() + '/../results/lda/jobcomp/'
    if not os.path.exists(res_path):
        os.makedirs(res_path)
    res_file_path = res_path + "jobcomp.csv"
    res_file = Path(res_file_path)
    if res_file.is_file():
        os.remove(res_file_path)
#    job_count = 0
    q = Path(JOB_PATH)
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
            job_lda = ldamodel[job_bow]
            index = similarities.MatrixSimilarity(ldamodel[corpus])
            sims = index[job_lda]
            comps = texts.keys()
            comp_count = 0
            with open(res_file_path, mode="a") as text_file:
                for doc,sim in enumerate(sims):
                    text_file.write(str(job_count) + "," + str(comp_count) + "," + comps[doc] + "," + str(sim) + "\n")
                    comp_count += 1           
            job_count += 1
    

def cv_comp_sims():
    texts = read_comp_doc()
    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(texts.values())
        
    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in texts.values()]
    
    # generate LDA model
    ldamodel = models.ldamodel.LdaModel(corpus, num_topics=40, id2word = dictionary, passes=50)
    #print(ldamodel.print_topics(num_topics=5))
    cm = CoherenceModel(model=ldamodel, texts=texts.values(), dictionary=dictionary, coherence='c_v')
    print(cm.get_coherence())

    ## compute similarities for CVs 
    res_path = os.getcwd() + '/../results/lda/cvcomp/'
    if not os.path.exists(res_path):
        os.makedirs(res_path)
    res_file_path = res_path + "cvcomp.csv"
    res_file = Path(res_file_path)
    if res_file.is_file():
        os.remove(res_file_path)
    cv_count = 0
    for filename in glob.glob(CV_PATH + '*.json'):
            cv_text = clean(filename, 'json')
            cv_bow = dictionary.doc2bow(cv_text)
            cv_lda = ldamodel[cv_bow]
            index = similarities.MatrixSimilarity(ldamodel[corpus])
            sims = index[cv_lda]
            comps = texts.keys()
            comp_count = 0
            with open(res_file_path, mode="a") as text_file:
                for doc,sim in enumerate(sims):
                    text_file.write(str(cv_count) + "," + str(comp_count) + "," + comps[doc] + "," + str(sim) + "\n")
                    comp_count += 1           
            cv_count += 1




def read_job_doc():
    import json
    texts = {}
    q = Path(JOB_PATH)
    with q.open() as f:
        for line in f:
            json_obj = json.loads(line.strip())
            try:
                job_text = json_obj["description"]
                job_count = int(json_obj['jobid'])
            except:
                continue
            texts[job_count] = clean_text(job_text)
    return texts

def job_cv_sims():
    texts = read_job_doc()
    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(texts.values())
        
    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in texts.values()]
    
    # generate LDA model
    ldamodel = models.ldamodel.LdaModel(corpus, num_topics=40, id2word = dictionary, passes=50)
    #print(ldamodel.print_topics(num_topics=5))
    cm = CoherenceModel(model=ldamodel, texts=texts.values(), dictionary=dictionary, coherence='c_v')
    print(cm.get_coherence())

    res_path = os.getcwd() + '/../results/lda/jobcv/'
    if not os.path.exists(res_path):
        os.makedirs(res_path)
    res_file_path = res_path + "jobcv.csv"
    res_file = Path(res_file_path)
    if res_file.is_file():
        os.remove(res_file_path)
    ## compute similarities for CVs 
    cv_count = 0
    for filename in glob.glob(CV_PATH + '*.json'):
#        if cv_count < 6:
        cv_text = clean(filename, 'json')
        cv_bow = dictionary.doc2bow(cv_text)
        cv_lda = ldamodel[cv_bow]
        index = similarities.MatrixSimilarity(ldamodel[corpus])
        sims = index[cv_lda]
#            jobs = texts.keys()
        comp_count = 0
        with open(res_file_path, mode="a") as text_file:
            for doc,sim in enumerate(sims):
                text_file.write(str(cv_count) + "," + str(doc) + "," + str(sim) + "\n")
                comp_count += 1           
        cv_count += 1         
            

def visualize_topics():
#    import pyLDAvis   
    
    texts = read_comp_doc()
    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(texts.values())
        
    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in texts.values()]
    
    # generate LDA model
    ldamodel = models.ldamodel.LdaModel(corpus, num_topics=20, id2word = dictionary, passes=50)
    #print(ldamodel.print_topics(num_topics=5))
    cm = CoherenceModel(model=ldamodel, texts=texts.values(), dictionary=dictionary, coherence='c_v')
    print(cm.get_coherence())

    print('=Preparing data for visualisation ...')
    vis_data = pyLDAvis.gensim.prepare(ldamodel, corpus, dictionary, mds='mmds')
    print('=Visualizing prepared data ...')
    pyLDAvis.show(vis_data)

if __name__ == '__main__':
#    visualize_topics()
    job_comp_sims()
    cv_comp_sims()
    job_cv_sims()
