# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 17:06:44 2017

@author: user
"""

from boilerpipe.extract import Extractor

"""
    Extract text. Constructor takes 'extractor' as a keyword argument,
    being one of the boilerpipe extractors:
    - DefaultExtractor
    - ArticleExtractor
    - ArticleSentencesExtractor
    - KeepEverythingExtractor
    - KeepEverythingWithMinKWordsExtractor
    - LargestContentExtractor
    - NumWordsRulesExtractor
    - CanolaExtractor
"""

url = 'http://www.channelnewsasia.com/news/asiapacific/poor-and-on-their-own-south-korea-s-elderly-who-will-work-until/3607312.html'
html = 'C:\\Users\\user\\Documents\\spyderprojects\\selenium_project\\forbes.html'

#f = open(html, 'r')
#html = f.read()
#
#print html
#
#DefaultExtractor = Extractor(extractor='DefaultExtractor', html=html)
#print "DefaultExtractor:\n" + DefaultExtractor.getText() + "\n"
#
#ArticleSentencesExtractor = Extractor(extractor='ArticleSentencesExtractor', html=html)
#print "ArticleSentencesExtractor:\n" + ArticleSentencesExtractor.getText() + "\n"



#DefaultExtractor = Extractor(extractor='DefaultExtractor', url=url)
#print "DefaultExtractor:\n" + DefaultExtractor.getText() + "\n"
#
ArticleExtractor = Extractor(extractor='ArticleExtractor', url=url)
print "ArticleExtractor:\n" + ArticleExtractor.getText() + "\n"

ArticleSentencesExtractor = Extractor(extractor='ArticleSentencesExtractor', url=url)
print "ArticleSentencesExtractor:\n" + ArticleSentencesExtractor.getText() + "\n"

#KeepEverythingExtractor = Extractor(extractor='KeepEverythingExtractor', url=url)
#print "KeepEverythingExtractor:\n" + KeepEverythingExtractor.getText() + "\n"
#
##KeepEverythingWithMinKWordsExtractor = Extractor(extractor='KeepEverythingWithMinKWordsExtractor', url=url)
##print "KeepEverythingWithMinKWordsExtractor:\n" + KeepEverythingWithMinKWordsExtractor.getText() + "\n"
#
#LargestContentExtractor = Extractor(extractor='LargestContentExtractor', url=url)
#print "LargestContentExtractor:\n" + LargestContentExtractor.getText() + "\n"
#
#NumWordsRulesExtractor = Extractor(extractor='NumWordsRulesExtractor', url=url)
#print "NumWordsRulesExtractor:\n" + NumWordsRulesExtractor.getText() + "\n"
#
#CanolaExtractor = Extractor(extractor='CanolaExtractor', url=url)
#print "CanolaExtractor:\n" + CanolaExtractor.getText() + "\n"

#ascii_replace = orginal.encode('ascii', 'replace')
#ascii_replace.replace('\n', ' ').replace('?', '')