#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 13:54:53 2017

@author: alfred
"""

import sys
import re
import time
import pandas as pd
from seleniumdriver import SeleniumDriver
from contentscraper import ContentScraper
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import DBSCAN
from gensim.summarization import summarize


#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)

if __name__ == "__main__":
    
    try:
        search_topic = sys.argv[1]
    except IndexError:
        print "ERROR: Please enter your search topic in quotes \"\"."
        sys.exit()
    
    try:
        maxPage = int(sys.argv[2])
    except IndexError:
        print "WARNING: max_pages for searching is not defined, default will be used."
        maxPage = 3
        
    ##########################################################################################
    ##
    ## Crawling
    ##
    ##########################################################################################

    start_time = time.time()
    print("Start Crawling news articles...")
    
    seleniumDriver = SeleniumDriver()
    contentScraper = ContentScraper()

    link = seleniumDriver.search_newsLink(search_topic+ " news")
    
    page = 1
    df = pd.DataFrame()
    
    while page <= maxPage:
        print("Scraping Page %s..." % (page))
        page += 1
        link, results = seleniumDriver.crawl_newsLink(link)
        for row in results:
            print("Scraping: %s" % (row['URL']))
            contents = contentScraper.scrap_link_goose(row['URL'])
            if len(contents) > 0:
                ascii_replace = contents.encode('ascii', 'replace')
                ascii_replace = ascii_replace.replace('\n', ' ').replace('?', '')
                row['Contents'] = ascii_replace
            else:
                row['Contents'] = None
            df = df.append(row, ignore_index=True)

    seleniumDriver.kill()
    
    print("Crawling took %s seconds..." % (time.time() - start_time))
    
    #save data to csv
    df.to_csv(re.sub(" +", "", search_topic).lower()+".csv", encoding='utf-8')
    
    ##########################################################################################
    ##
    ## Features Extraction + Clustering
    ##
    ##########################################################################################
    start_time = time.time()
    
    df = df.dropna()
    
    vectorizer = CountVectorizer(max_df=0.9, min_df=2, stop_words='english')
    matrix = vectorizer.fit_transform(df['Contents'])
    
    lda = LatentDirichletAllocation(n_topics=10,
                                max_iter=10,
                                doc_topic_prior=0.4,
                                topic_word_prior=0.4,
                                learning_method='online',
                                learning_offset=50.,
                                verbose=1,
                                random_state=1)
    matrix = lda.fit_transform(matrix)
    
    dbscan = DBSCAN(eps=0.1, min_samples=3)
    dbscan.fit(matrix)
    
    print("Clustering took %s seconds..." % (time.time() - start_time))
    
    df['dbscan_labels'] = dbscan.labels_
    
    ##########################################################################################
    ##
    ## Summarization
    ##
    ##########################################################################################
    start_time = time.time()
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
        print("Number of articles: %s" % (len(summarized_article)))
        print("Titles:")
        for i in range(0, len(titles)):
            print("%s) %s" % (i+1, titles[i]))
        print("Summarized Contents: \n%s\n" % (summarized_text))
    
    print("Summarization took %s seconds..." % (time.time() - start_time))
    