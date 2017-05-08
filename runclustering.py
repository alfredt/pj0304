#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 09:12:54 2017

@author: alfred
"""

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import tokenizer
import clustering

def RunClustering(df, eps):
    
    df = df.dropna()
    
    vectorizer = CountVectorizer(max_df=0.9, min_df=3, stop_words='english', max_features=500)
    
#    vectorizer = TfidfVectorizer(max_df=0.9, min_df=3, stop_words='english')
    
    matrix = vectorizer.fit_transform(df['Contents'])
    
    lda = LatentDirichletAllocation(n_topics=20,
                                max_iter=15,
                                doc_topic_prior=0.4,
                                topic_word_prior=0.4,
                                learning_method='online',
                                learning_offset=50.,
                                verbose=1,
                                random_state=1)
    matrix = lda.fit_transform(matrix)
    
    dbscan = DBSCAN(eps=eps, min_samples=3)
    dbscan.fit(matrix)
    
    df['dbscan_labels'] = dbscan.labels_
    
#    print df[['Title','dbscan_labels']]
    
    return df