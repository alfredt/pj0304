# -*- coding: utf-8 -*-
"""
Created on Thu Mar 09 11:10:16 2017

@author: user
"""

import logging
import mongodb as mg
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.cluster import DBSCAN
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np
import preprocessing_nltk as pNLTK
from pandas import ExcelWriter

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger('DBSCAN')
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
    
    logger.debug("DBSCAN started")
    
    config = {}
    execfile("C:\\Users\\user\\Documents\\spyderprojects\\selenium_project\\configFile.conf", config)
    
    writer = ExcelWriter('DBCAN_Results_Preprocessed'+str(30)+'_minDF.xlsx')
    
    name_database = config['database']
    name_collection = config['collection']
    
    mongoClient, db = mg.init_mongo(name_database)
    
    # extract dataset from MongoDB
    logger.info("Loading dataset...")
    data = mg.extract_news(db, name_collection)
    news = pd.DataFrame(list(data))
    
    # perform LDA
    # preprocessing & lemmatizing dataset using NLTK, extracting only Nouns
    logger.info("Preprocessing & Lemmatizing dataset...")
    news['ProcessedContents'] = pNLTK.preprocess_pos(news['Contents'], 'NN(P|PS)')
    
    tf_vectorizer = CountVectorizer(max_df=0.85, min_df=3, stop_words='english')
    
    tf_matrix = tf_vectorizer.fit_transform(news['ProcessedContents'])
    
#    lda = LatentDirichletAllocation(n_topics=20,
#                                    max_iter=15,
#                                    doc_topic_prior=0.4,
#                                    topic_word_prior=0.6,
#                                    learning_method='online',
#                                    learning_offset=50.,
#                                    verbose=1,
#                                    random_state=1)
#    
#    lda_result = lda.fit_transform(tf_matrix)
    
    # fitting the DBSCAN model with tf-idf features
    logger.info("Fitting the DBSCAN model with tf-idf features")
    for eps in np.arange(0.1, 2, 0.1):
        
        logger.info("Fitting using eps: %s", eps)
        
        dbscan_model = DBSCAN(eps=eps, min_samples=3)
        dbscan_model.fit(tf_matrix)
        news[eps] = dbscan_model.labels_
    
    news.to_excel(writer, "News Article")
    writer.save()
    
    logger.debug("DBSCAN ended")