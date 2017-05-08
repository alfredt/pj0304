# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 15:43:57 2017

@author: user
"""

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

cv = CountVectorizer(min_df=0, stop_words="english", max_features=50)
counts = cv.fit_transform([line]).toarray().ravel()                                                  
words = np.array(cv.get_feature_names()) 
# normalize                                                                                                                                             
counts = counts / float(counts.max())