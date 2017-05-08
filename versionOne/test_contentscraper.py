# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 17:06:44 2017

@author: user
"""

from boilerpipe.extract import Extractor
from goose import Goose
from readability import Document
import requests

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

url = 'https://techcrunch.com/2017/02/13/mit-speech-chip/' #BadStatusLine from boilerpipurle

url = "http://www.forbes.com/sites/trevorclawson/2017/02/23/finding-a-voice-can-a-uk-startup-compete-with-its-heavy-hitters-in-the-speech-recognition-market/"

url = "https://nakedsecurity.sophos.com/2017/03/03/researcher-uses-googles-speech-tools-to-skewer-google-recaptcha/"

url = "http://www.natureworldnews.com/articles/32595/20161123/microsoft-officially-makes-first-humanly-accurate-speech-recognition-tech.htm"

url = "http://www.businessinsider.com/ibm-edges-closer-to-human-speech-recognition-2017-3"
#ArticleExtractor = Extractor(extractor='ArticleExtractor', url=url)
#print "ArticleExtractor:\n" + ArticleExtractor.getText() + "\n"

ArticleSentencesExtractor = Extractor(extractor='ArticleSentencesExtractor', url=url)
print ArticleSentencesExtractor.getText()

article = Goose().extract(url=url)
print article.cleaned_text

document = Document(requests.get(url))
document.content()