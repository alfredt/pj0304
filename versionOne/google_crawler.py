# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 10:29:15 2017

@author: user
"""

import time
import logging
import selenium_driver as sd
import random

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger('google-crawler')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

if __name__ == "__main__":
    
    logger.debug("Google Crawler started")
    
    config = {}
    execfile("/home/alfred/Projects/pj0304/configFile.conf", config)
    
    driver = sd.init_driver()
    keywords = config['keywords']
    news_link = sd.google_search_keywords_news_link(driver, keywords=keywords)
    
    while True:
        if news_link != False:
            logger.debug("News Link: %s", news_link)
            break
        else:
            news_link = sd.google_search_keywords_news_link(driver, keywords=keywords)
    
    time.sleep(random.randrange(3, 5))
    pageNumber, maxPage = 1, 40
    
    while pageNumber <= maxPage:
        logger.debug("Page: %s", pageNumber)
        news_link = sd.crawl_newsLinks(driver, news_link)
        time.sleep(random.randrange(3, 5))  
        logger.debug("Page: %s crawling completed", pageNumber)
        pageNumber += 1
        
    time.sleep(5)
    driver.quit()
    logger.debug("Google Crawler stopped")