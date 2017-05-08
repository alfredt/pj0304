#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 11:05:54 2017

@author: alfred
"""

from runcrawling import WebCrawler
import tokenizer
import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import math
import clustering
import runsummarization

def KMeans_Search(searchTopic, maxPage):
    
    
    print("Start Crawling news articles...")
    webCrawler = WebCrawler()
    df = webCrawler.crawl(searchTopic, maxPage)
    
    df = df.dropna()
    
    stopwords_list = stopwords.read_stopwords()
    
    vectorizer = TfidfVectorizer(min_df=0.1,
                                 max_df=0.9,
                                 max_features=None,
                                 stop_words=stopwords_list,
                                 use_idf=True,
                                 tokenizer=tokenizer.tokenize_and_stem,
                                 ngram_range=(1,3))
    
    X = vectorizer.fit_transform(df['Contents'])
    
    n_clusters = int(math.ceil(math.sqrt(len(df))))
    print("Total # of articles crawled: %s | # of Clusters: %s" % (len(df), n_clusters))
    
    df['Cluster'] = clustering.RunKMeans(X, n_clusters)
    
    group_by = df.groupby(['Cluster'])['Contents'].count().sort_values(ascending=False).index.tolist()
    
    #hottest topic
    print("Top 2 clusters...")
    #1
    runsummarization.RunSummarization2(df, group_by[0], True)
    
    #2
    runsummarization.RunSummarization2(df, group_by[1], True)
    
    #latest topic
    print("Least number of article cluster...")
    runsummarization.RunSummarization2(df, group_by[-1], True)
    
if __name__ == "__main__":
    
    searchTopic = "Asean Summit"
    maxPage = 2
        
#    main(searchTopic, maxPage)
    KMeans_Search(searchTopic, maxPage)
