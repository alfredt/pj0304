#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 09:09:34 2017

@author: alfred
"""
import sys
import time
import runcrawling, runclustering, runsummarization 
from mainTest2 import KMeans_Search

def main(searchTopic, maxPage):
    
    start_time = time.time()
    print("Start Crawling news articles...")
    webCrawler = runcrawling.WebCrawler(crawlContents=True)
    df = webCrawler.crawl(searchTopic, maxPage)
    print("Crawling took %s seconds..." % (time.time() - start_time))
    start_time = time.time()
    df = runclustering.RunClustering(df, eps=0.1)
    print("Clustering took %s seconds..." % (time.time() - start_time))
    runsummarization.RunSummarization(df)

if __name__ == "__main__":
    
    try:
        searchTopic = sys.argv[1]
    except IndexError:
        print "ERROR: Please enter your search topic in quotes \"\"."
        sys.exit()
    
    try:
        maxPage = int(sys.argv[2])
    except IndexError:
        print "WARNING: max_pages for searching is not defined, default will be used."
        maxPage = 3
        
#    main(searchTopic, maxPage)
    KMeans_Search(searchTopic, maxPage)
    