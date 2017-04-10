# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 14:40:47 2017

@author: user
"""

import logging
import pymongo

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger('mongodb')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

def init_mongo(database):
    client = pymongo.MongoClient('localhost', 27017)
    db = client[database]
    logger.info("MongoDB initiated, Database: %s", database)
    return client, db

def insert_doc(db, collection, doc):
    col = db[collection]
    try:
        col.insert_one(doc)
    except pymongo.errors.DuplicateKeyError:
        logger.error("DuplicateKeyError: News link had been crawled & saved previously")
    except:
        logger.exception("error")
    else:
        logger.info("document inserted into %s", collection)
        
def extract_crawled_links(db, collection):
    col = db[collection]
    data = col.find({'Status':{'$exists':False}})
    return data

def update_doc_content(db, collection, _id, content, status):
    col = db[collection]
    col.update({'_id':_id}, {'$set':{'Contents':content, 'Status':status}}, upsert=True)
    
def extract_news(db, collection):
    col = db[collection]
    data = col.find({'Status': 1}, {'_id': 0, 'Contents': 1, 'Title':1, 'DirectLink':1})
    return data
    
#if __name__ == "__main__":
#    
#    logger.debug("Started")
#    
##    new_doc = {'Date': u'30 Jan 2017',
##               'Summary': u'There is too much hype surrounding deep learning, and it\'s not the right tool ... Instead of turning to deep learning, Sundown AI, established in ...',
##               'DirectLink': u'http://www.techrepublic.com/article/deep-learning-for-customer-service-is-overhyped-how-one-company-did-it-faster-and-cheaper/',
##               'Title': u'Deep learning for customer service is overhyped: How one company ...'}
##    
#    mongoClient, database = init_mongo("google")
##    insert_doc(database, "CrawledLinks",new_doc)
#
#    data = extract_news(database, "news")
#    for i in data:
#        print i