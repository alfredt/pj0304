# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 09:40:12 2017

@author: user
"""

import logging
import mongodb as mg
import pandas as pd
from pandas import ExcelWriter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import preprocessing_nltk as pNLTK
#from sklearn.cluster import DBSCAN
#import numpy as np
import time

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger('NMF')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

n_topics = 15
n_top_words = 15
max_features = 1000

def print_top_words(model, feature_names, n_top_words):
    lst = []
    for topic_idx, topic in enumerate(model.components_):
#        print("Topic #%d:" % topic_idx)
        terms = " ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]])
#        print terms
        dic = {}
        dic['Topic'] = topic_idx
        dic['Terms'] = terms
        lst.append(dic)
    return pd.DataFrame(lst)
    
if __name__ == "__main__":
    
    logger.debug("NMF started...")
#    writer = ExcelWriter('NMF_LDA_Results_'+str(n_topics)+'_2.xlsx')
    
    config = {}
    execfile("C:\\Users\\user\\Documents\\spyderprojects\\selenium_project\\configFile.conf", config)
    
    writer = ExcelWriter('NMF_Results_'+str(n_topics)+'.xlsx')
    
    name_database = config['database']
    name_collection = config['collection']
    
    mongoClient, db = mg.init_mongo(name_database)
    
    # extract dataset from MongoDB
    logger.info("Loading dataset...")
    data = mg.extract_news(db, name_collection)
    news = pd.DataFrame(list(data))
    
    # preprocessing & lemmatizing dataset using NLTK, extracting only Nouns
    logger.info("Preprocessing & Lemmatizing dataset...")
    news['ProcessedContents'] = pNLTK.preprocess_pos(news['Contents'], 'NN(P|PS)')
    
    # use tf-idf features for NMF
    logger.info("Extracting tf-idf features for NMF...")
    tfidf_vectorizer = TfidfVectorizer(max_df = 0.85,
                                       min_df = 3,
#                                       ngram_range = (1,2),
#                                       max_features = max_features,
                                       stop_words = 'english')
    
    tfidf_matrix = tfidf_vectorizer.fit_transform(news['ProcessedContents'])
    
    logger.info("Fitting the NMF model with tf-idf features...")
    
    nmf = NMF(n_components=n_topics,
              random_state=1,
              alpha=.1,
              l1_ratio=.5)
    
    nmf_result = nmf.fit_transform(tfidf_matrix)
    
    tfidf_feature_names = tfidf_vectorizer.get_feature_names()
    logger.info("Preparing for NMF Topic-Term Matrix with %s top-words...", n_top_words)
    df_nmf_topic_term = print_top_words(nmf, tfidf_feature_names, n_top_words)
    
    logger.info("Preparing for NMF Doc-Topic Matrix...")
    df_nmf_doc_topic = news
#    print nmf_result.argmax(axis=1)
    df_nmf_doc_topic['topic'] = nmf_result.argmax(axis=1)
#    print df_nmf_doc_topic
    
    df_nmf_doc_topic.to_excel(writer, "NMF Doc-Topic")
    df_nmf_topic_term.to_excel(writer, "NMF Topic-Term")
    
    writer.save()
    
    logger.debug("NMF completed...")
    