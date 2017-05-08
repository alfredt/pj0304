# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 12:27:15 2017

@author: user
"""

import logging
import mongodb as mg
import pandas as pd
import preprocessing_nltk as pNLTK
from pandas import ExcelWriter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
#from sklearn.cluster import DBSCAN
#import numpy as np
import time

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger('LDA')
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
    
    logger.debug("LDA started...")
#    writer = ExcelWriter('NMF_LDA_Results_'+str(n_topics)+'_2.xlsx')
    
    config = {}
    execfile("C:\\Users\\user\\Documents\\spyderprojects\\selenium_project\\configFile.conf", config)
    
    writer = ExcelWriter('LDA_Results_Preprocessed'+str(n_topics)+'_minDF.xlsx')
    
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
    
    
    for min_df in range(1,5):
        logger.info("Extracting tf features for LDA... min_df: %s", min_df)
        tf_vectorizer = CountVectorizer(max_df=0.95,
                                        min_df=min_df,
    #                                    max_features=max_features,
                                        stop_words='english')
        
#        tf_matrix = tf_vectorizer.fit_transform(news['Contents'])
        tf_matrix = tf_vectorizer.fit_transform(news['ProcessedContents'])
    
        logger.info("Fitting the LDA model with tf features...")
        lda = LatentDirichletAllocation(n_topics=n_topics,
                                        max_iter=20,
                                        doc_topic_prior=0.4,
                                        topic_word_prior=0.4,
                                        learning_method='online',
                                        learning_offset=50.,
                                        verbose=1,
                                        random_state=1)
        lda_result = lda.fit_transform(tf_matrix)
    
        tf_feature_names = tf_vectorizer.get_feature_names()
        logger.info("Preparing for LDA Topic-Term Matrix with %s top-words...", n_top_words)
        df_lda_topic_term = print_top_words(lda, tf_feature_names, n_top_words)
        
        logger.info("Preparing for LDA Doc-Topic Matrix...")
        df_lda_doc_topic = news
        df_lda_doc_topic['topic'] = lda_result.argmax(axis=1)
        
        df_lda_doc_topic.to_excel(writer, "LDA Doc-Topic min_df "+str(min_df))
        df_lda_topic_term.to_excel(writer, "LDA Topic-Term min_df "+str(min_df))
        
    writer.save()
    
    logger.debug("LDA completed...")
    