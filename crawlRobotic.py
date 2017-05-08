#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 10:42:40 2017

@author: alfred
"""

import time
import runcrawling
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer

if __name__ == "__main__":
    
    searchTopic = "singapore robotics"
    maxPage = 5
    
    additional_stopwords = "singapore robot robots robotic robotics wa work people port" 
    
    webCrawler = runcrawling.WebCrawler(crawlContents=True)
    start_time = time.time()
    print("Start Crawling news articles...")
    df = webCrawler.crawl(searchTopic, maxPage)
    print("Crawling took %s seconds..." % (time.time() - start_time))
    
    with open('./stopwords_en.txt') as f:
        stopwords = f.readlines()
        stopwords = [x.strip() for x in stopwords]
    
    stopwords.extend(additional_stopwords.split())
    
    df = df.dropna()
    
    wordnet_lemmatizer = WordNetLemmatizer()
    
    contents = df['Contents']
    new_contents = ""
    for content in contents:
        content = content.split()
        new_content = ""
        for word in content:
            new_word = wordnet_lemmatizer.lemmatize(word)
            new_content += new_word + " "
        new_contents += new_content + " "
    
    cv = CountVectorizer(token_pattern=u'[a-zA-Z]{4,}', max_df=0.9, min_df=2, stop_words=stopwords, ngram_range=(1,3))
    tv = TfidfVectorizer(token_pattern=u'[a-zA-Z]{4,}', max_df=0.9, min_df=2, stop_words=stopwords, ngram_range=(1,3))
    
    X = cv.fit_transform(contents)
    cv_freq = zip(cv.get_feature_names(), np.asarray(X.sum(axis=0)).ravel())
    
    Y = tv.fit_transform(contents)
    tv_freq = zip(tv.get_feature_names(), tv.idf_)
    
    wc = WordCloud(max_words=100, width=600, height=400, background_color="black", margin=10, prefer_horizontal=1.0)
    
    wc.generate_from_frequencies(cv_freq)
    plt.figure(dpi=300, figsize=(3,2))
    plt.imshow(wc)
    plt.axis("off")
    
    wc.generate_from_frequencies(tv_freq)
    plt.figure(dpi=300, figsize=(3,2))
    plt.imshow(wc)
    plt.axis("off")
    
#    title_array = df['Title']
#    summary_array = df['Summary']
#    
#    title_string = ""
#    summary_string = ""
#    
#    for t in title_array:
#        title_string += "".join(t) + " "
#        
#    for s in summary_array:
#        summary_string += "".join(s) + " "
#        
#    title_string = title_string.lower()
#    summary_string = summary_string.lower()
#    
#    searchTopic = searchTopic.split()
#    for k in searchTopic:
#        title_string = re.sub(k, '', title_string)
#        summary_string = re.sub(k, '', summary_string)
#    
#    wordcloud = WordCloud(max_font_size=40).generate(title_string)
#    plt.figure()
#    plt.imshow(wordcloud, interpolation="bilinear")
#    plt.axis("off")
#    plt.show()
#    
#    wordcloud = WordCloud(max_font_size=40).generate(summary_string)
#    plt.figure()
#    plt.imshow(wordcloud, interpolation="bilinear")
#    plt.axis("off")
#    plt.show()
