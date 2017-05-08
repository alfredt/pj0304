# -*- coding: utf-8 -*-
"""
Created on Thu Mar 02 17:07:12 2017

@author: user
"""

import logging
import random
from boilerpipe.extract import Extractor
import mongodb as mg
import time
import urllib2, httplib
import socket

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger('boilerpipe')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

if __name__ == "__main__":
    
    logger.debug("Boilerpipe Crawler started")
    
    config = {}
    execfile("/home/alfred/Projects/pj0304/configFile.conf", config)
    
    no_crawling_list = ['forbes', 'techcrunch']
    
    name_database = config['database']
    name_collection = config['collection']
    
    mongoClient, db = mg.init_mongo(name_database)
    
    data = mg.extract_crawled_links(db, name_collection)
    
    for d in data:
        time.sleep(random.randrange(1, 2))
        logger.info("Title: %s", d['Title'])
        logger.info("Link: %s", d['DirectLink'])
        skip = False
        keepCrawling = True
        retry = 0
        
        for not_crawling in no_crawling_list:
            if not_crawling in d['DirectLink']:
                logger.warn("DirectLink is in not crawling list (%s) ...", not_crawling)
                mg.update_doc_content(db, name_collection, d['_id'], None, "NoCrawlingList")
                skip = True
        
        if not skip:
            while keepCrawling:
                try:        
                    extractor = Extractor(extractor='ArticleSentencesExtractor', url=d['DirectLink'])
                    text = extractor.getText()
                    if len(text) > 0:
                        ascii_replace = text.encode('ascii', 'replace')
                        ascii_replace = ascii_replace.replace('\n', ' ').replace('?', '')
                        mg.update_doc_content(db, name_collection, d['_id'], ascii_replace, 1)
                        logger.info("Contents updated...")
                    else:
                        mg.update_doc_content(db, name_collection, d['_id'], None, 0)
                        logger.warn("Zero contents updated...")
                    keepCrawling = False
                except urllib2.HTTPError:
                    time.sleep(random.randrange(9, 15))
                    if retry == 3:
                        logger.error("HTTP Error 404 - Retry exceeded... Stop trying... ")
                        mg.update_doc_content(db, name_collection, d['_id'], None, "HTTPError404")
                        keepCrawling = False
                    else:
                        retry += 1
                        logger.warn("HTTP Error 404 - Retry: %s - re-crawl webpage again...", retry)
                except httplib.BadStatusLine:
                    logger.error("BadStatusLine")
                    mg.update_doc_content(db, name_collection, d['_id'], None, "BadStatusLine")
                    keepCrawling = False
                except socket.timeout:
                    time.sleep(random.randrange(3, 5))
                    if retry == 3:
                        logger.error("Socket Timeout - Retry exceeded... Stop trying... ")
                        keepCrawling = False
                    else:
                        retry += 1
                        logger.warn("HTTP Error 404 - Retry: %s - re-crawl webpage again...", retry)
                except urllib2.URLError:
                        logger.error("SSL: CERTIFICATE_VERIFY_FAILED... ")
                        mg.update_doc_content(db, name_collection, d['_id'], None, "SSLCertVerifyFailed")
                        keepCrawling = False
                    
                
    logger.debug("Boilerpipe Crawler endeded")