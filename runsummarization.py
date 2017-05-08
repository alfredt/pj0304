#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 09:23:21 2017

@author: alfred
"""
import re
from gensim.summarization import summarize
import tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import cosine

def RunSummarization(df):
    
    max_cluster = max(df['dbscan_labels']) + 1
    print("There are total of %s clusters..." % (max_cluster))
    
    for cluster_id in range(0, max_cluster):
        print("Cluster: %s" % (cluster_id))
        #summarization on each article then on whole cluster
        summarized_article = list()
        titles = list()
        for index, row in df[df['dbscan_labels']==cluster_id].iterrows():
            summarized_article.append(summarize(re.sub(' +',' ', row['Contents']), ratio=0.6))
            titles.append(row['Title'])
        
        summarized_article = re.sub(' +',' ', " ".join(summarized_article))
#        summarized_text2 = summarize(summarized_article, ratio=0.2)
        summarized_text = summarize(summarized_article, word_count=300)
        print("Number of articles: %s" % (len(titles)))
        print("Titles:")
        for i in range(0, len(titles)):
            print("%s) %s" % (i+1, titles[i]))
        print("Summarized Contents:\n%s\n" % (summarized_text))
        
def RunSummarization2(df, cluster_id, print_title=False, word_count=300, split=False, cos_threshold=0.85):
    
    summarized_article = list()
    titles = list()
    
    for index, row in df[df['Cluster']==cluster_id].iterrows():
        summarized_article.append(re.sub(' +',' ', row['Contents']))
        titles.append(row['Title'])
        
    removed_duplicates_sentences = RemoveDuplicatesSentences(summarized_article, threshold=cos_threshold)
        
    summarized_article = re.sub(' +',' ', " ".join(removed_duplicates_sentences))
    summarized_text = summarize(summarized_article, word_count=word_count, split=split)
        
    print("Number of articles: %s" % (len(titles)))
    
    if print_title:
        print("Titles:")
        for i in range(0, len(titles)):
            print("%s) %s" % (i+1, titles[i]))
    print("Summarized Contents:\n%s\n" % (summarized_text))
    return summarized_text
    
def RemoveDuplicatesSentences(sentences, threshold):
    
    vectorizer = TfidfVectorizer(tokenizer=tokenizer.tokenize_and_lemmatizer)
    Y = vectorizer.fit_transform(sentences)
    Y = Y.toarray()
    distance = 1-pairwise_distances(Y, metric="cosine")
    
    #finding the sententces to remove
    remove_sentences_id = list()
    for i in range(0, distance.shape[0]):
#        print "i: " + str(i)
        if i in remove_sentences_id:
            continue
        else:
            for j in range(i, distance[i].shape[0]):
                if distance[i][j] > threshold and i != j:
#                    print str(distance[i][j])
#                    print "over"
                    remove_sentences_id.append(j)
#                else:
#                    print str(distance[i][j])
    for i in remove_sentences_id:
        sentences.remove(sentences[i])
    
    return sentences        