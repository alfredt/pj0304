#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 11:04:42 2017

@author: alfred
"""
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans

def RunLDA(X, n_topics, max_iter, doc_topic_prior, topic_word_pior):
    
    lda = LatentDirichletAllocation(n_topics=n_topics,
                                    max_iter=max_iter,
                                    doc_topic_prior=doc_topic_prior,
                                    topic_word_prior=topic_word_pior,
                                    learning_method='online',
                                    learning_offset=50.,
                                    verbose=1,
                                    random_state=1)
    y = lda.fit(X)
    return y

def RunDBSCAN(X, eps, min_sample):
    
    dbscan = DBSCAN(eps=eps, min_samples=min_sample)
    dbscan.fit(X)   
    y = dbscan.labels_
    return y

def RunKMeans(X, n_clusters):
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    kmeans.fit(X)
    y = kmeans.labels_
    return y