#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 13:17:35 2017

@author: alfred
"""

def read_stopwords():
    with open('./stopwords_en.txt') as f:
        stopwords = f.readlines()
        stopwords = [x.strip() for x in stopwords]
    return stopwords