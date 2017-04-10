# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 15:43:57 2017

@author: user
"""

import pymongo
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

client = pymongo.MongoClient('localhost', 27017)
db = client['google']
col = db['news']
data = col.find({'Status': 1}, {'_id': 0, 'Contents': 1, 'Title':1, 'DirectLink':1})

news = pd.DataFrame(list(data))
cv = CountVectorizer(min_df=0, stop_words="english", max_features=200)
counts = cv.fit_transform(news['Contents'])
counts_toArray = counts.toarray()
counts_toRavel = counts_toArray.ravel()

words = np.array(cv.get_feature_names())
 