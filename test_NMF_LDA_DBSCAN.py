# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 11:17:03 2017

@author: user
"""
import logging
import mongodb as mg
import pandas as pd
from pandas import ExcelWriter
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
#from sklearn.cluster import DBSCAN
#import numpy as np
import time

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger('NMF_LDA')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

n_topics = 15
n_top_words = 15
max_features = 500

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
    
    logger.debug("NMF-LDA started...")
    writer = ExcelWriter('NMF_LDA_Results_'+str(n_topics)+'_2.xlsx')
    
    config = {}
    execfile("C:\\Users\\user\\Documents\\spyderprojects\\selenium_project\\configFile.conf", config)
    
    name_database = config['database']
    name_collection = config['collection']
    
    mongoClient, db = mg.init_mongo(name_database)
    
    # extract dataset from MongoDB
    logger.info("Loading dataset...")
    data = mg.extract_news(db, name_collection)
    news = pd.DataFrame(list(data))
    
    # use tf-idf features for NMF
    logger.info("Extracting tf-idf features for NMF...")
    tfidf_vectorizer = TfidfVectorizer(max_df=0.95,
                                       min_df=3,
                                       max_features=max_features,
                                       stop_words='english')
    
    tfidf_matrix = tfidf_vectorizer.fit_transform(news['Contents'])
    
    # use tf features for LDA
    logger.info("Extracting tf features for LDA...")
    tf_vectorizer = CountVectorizer(max_df=0.95,
                                    min_df=3,
                                    max_features=max_features,
                                    stop_words='english')
    
    tf_matrix = tf_vectorizer.fit_transform(news['Contents'])
    
    ########################################################################################
    ###
    ### NMF Modeling
    ###
    ########################################################################################
    logger.info("Fitting the NMF model with tf-idf features...")
    nmf = NMF(n_components=n_topics,
              random_state=1,
              alpha=.1,
              l1_ratio=.5)
    nmf_result = nmf.fit_transform(tfidf_matrix)
#    nmf_component = nmf.components_
    
#    print("\nTopics in NMF model:")
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
    
    time.sleep(5)
    
    ########################################################################################
    ###
    ### LDA Modeling
    ###
    ########################################################################################
    logger.info("Fitting the LDA model with tf features...")
    lda = LatentDirichletAllocation(n_topics=n_topics,
                                    max_iter=5,
                                    learning_method='online',
                                    learning_offset=50.,
                                    random_state=1)
    lda_result = lda.fit_transform(tf_matrix)
#    lda_component = lda.components_
    
#    print("\nTopics in LDA model:")
    tf_feature_names = tf_vectorizer.get_feature_names()
    logger.info("Preparing for LDA Topic-Term Matrix with %s top-words...", n_top_words)
    df_lda_topic_term = print_top_words(lda, tf_feature_names, n_top_words)
    
    logger.info("Preparing for LDA Doc-Topic Matrix...")
    df_lda_doc_topic = news
#    print lda_result.argmax(axis=1)
    df_lda_doc_topic['topic'] = lda_result.argmax(axis=1)
#    print df_lda_doc_topic
    
    df_lda_doc_topic.to_excel(writer, "LDA Doc-Topic")
    df_lda_topic_term.to_excel(writer, "LDA Topic-Term")
    writer.save()
    
    logger.debug("NMF-LDA completed...")
    
    
    
#    # fitting the DBSCAN model with tf-idf features
#    logger.info("Fitting the DBSCAN model with tf-idf features")
#    for eps in np.arange(0.1, 2, 0.1):
#        
#        logger.info("Fitting using eps: %s", eps)
#        
#        dbscan_model = DBSCAN(eps=eps, min_samples=2)
#        dbscan_model.fit(tfidf_matrix)
#        news[eps] = dbscan_model.labels_
#    
#    logger.debug("DBSCAN ended")