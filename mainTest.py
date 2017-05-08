#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 10:51:13 2017

@author: alfred
"""

import time
import runcrawling, runclustering, runsummarization

if __name__ == "__main__":
    
    searchTopic = "singapore robotics"
    maxPage = 1
    
    start_time = time.time()
    print("Start Crawling news articles...")
    webCrawler = runcrawling.WebCrawler()
    df = webCrawler.crawl(searchTopic, maxPage)
    
    
    print("Crawling took %s seconds..." % (time.time() - start_time))
    start_time = time.time()
    df = runclustering.RunClustering(df, 0.2)
    print("Clustering took %s seconds..." % (time.time() - start_time))
    runsummarization.RunSummarization(df)