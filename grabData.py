# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 16:00:44 2017

@author: user
"""

import logging
import mongodb as mg
import pandas as pd

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger('grabData')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

config = {}
execfile("C:\\Users\\user\\Documents\\spyderprojects\\selenium_project\\configFile.conf", config)

def getData():
    
    name_database = config['database']
    name_collection = config['collection']
    
    mongoClient, db = mg.init_mongo(name_database)
    data = mg.extract_news(db, name_collection)
    news = pd.DataFrame(list(data))
    logger.info("Returning data...")
    return news
    
    