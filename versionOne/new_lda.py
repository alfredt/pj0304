# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 15:26:26 2017

@author: user
"""

import pymongo
import pandas as pd
import preprocessing_nltk as pNLTK

from pandas import ExcelWriter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import DBSCAN
import numpy as np
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import cosine
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import time

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

print "loading dataset from Mongo..."
client = pymongo.MongoClient('localhost', 27017)
db = client["google"]
col = db["speech"]
#data = col.find({'Status': 1,'Date':{'$gte':'2017-03-01'}}, {'_id': 0, 'Contents': 1, 'Title':1, 'DirectLink':1, 'Summary':1})
data = col.find({'Status': 1}, {'_id': 0, 'Contents': 1, 'Title':1, 'DirectLink':1, 'Summary':1})

print "convert Mongo cursor to DF..."
df = pd.DataFrame(list(data))

print "cleaning contents now..."
df['ProcessedContents'] = pNLTK.preprocess_pos(df['Contents'], 'NN(P|PS)')

print "preparing count vectorizer..."
tf_vectorizer = CountVectorizer(max_df=0.9,
                                min_df=2,
#                               max_features=max_features,
                                token_pattern='[A-Za-z]{3,}|[A-Z]{2,}',
                                stop_words='english')

tf_matrix = tf_vectorizer.fit_transform(df['ProcessedContents'])

print "lda model done now..."
lda = LatentDirichletAllocation(n_topics=20,
                                max_iter=15,
                                doc_topic_prior=0.4,
                                topic_word_prior=0.4,
                                learning_method='online',
                                learning_offset=50.,
                                verbose=1,
                                random_state=1)

lda_result = lda.fit_transform(tf_matrix)

print "dbscan model done now..."
dbscan_model = DBSCAN(eps=0.1, min_samples=3)
dbscan_model.fit(lda_result)
df['dbscan_labels'] = dbscan_model.labels_

max_cluster = max(df['dbscan_labels'])

print "There are total of "+str(max_cluster+1)+" clusters..."

for cluster_id in range(0, max_cluster+1):
#    cluster_id = 1
    print "Cluster ID: "+str(cluster_id)+"..."
    subset_df = df[df['dbscan_labels']==cluster_id]
    subset_df = subset_df.reset_index()
    subset_vectorizer = CountVectorizer(max_df=1.0,
                                        min_df=1,
                                        max_features=500,
                                        token_pattern='[A-Za-z]{3,}|[A-Z]{2,}',
                                        stop_words='english')
    matrix = subset_vectorizer.fit_transform(subset_df['ProcessedContents'])
    matrix_array = matrix.toarray()
    distance = 1-pairwise_distances(matrix_array, metric="cosine")
    distance_sum = distance.sum(axis=1)
    distance_average = (distance_sum - 1)/(distance.shape[0] - 1)
    rank = []
    
    if len(subset_df) > 3:
        while len(rank) < 3:
            max_id = distance_average.argmax()
            distance_average[max_id] = 0
            rank.append(max_id)
    else:
        rank.append(distance_average.argmax())
        
    #wordcloud
    text = str(subset_df['ProcessedContents'])
    wordcloud = WordCloud().generate(text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    
    time.sleep(15)
    
    print "Top Ranked Document(s) for Cluster: " + str(cluster_id)
    for i in rank:
        rank_doc = subset_df.loc[i]
        print "Title: " + str(rank_doc['Title'])
        print "Summary: " + str(rank_doc['Summary'])
        print "URL: " + str(rank_doc['DirectLink'])
        print ""
    
    time.sleep(3)
        

    