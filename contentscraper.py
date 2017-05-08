#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 16:38:53 2017

@author: alfred
"""

from goose import Goose
from boilerpipe.extract import Extractor

class ContentScraper(object):
     
    def __init__(self):
        self.engine = Goose()
        
    def scrap_link_goose(self, url):
        article = self.engine.extract(url=url)
        return article.cleaned_text
    
    def scrap_link_boilerpipe(url):
        try:
            extractor = Extractor(extractor='ArticleSentencesExtractor', url=url)
            return extractor.getText()
        except:
            return False