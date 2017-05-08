# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 15:56:29 2017

@author: user
"""

import nltk
import re
from nltk.stem.wordnet import WordNetLemmatizer

#pos_condition = re.compile('NN*|JJ*') #with Adjective & Nouns
#pos_condition = re.compile('NN*')

def preprocess_pos(contents, regrex):

    processed_contents = []
    wordnet_lemmatizer = WordNetLemmatizer()
    pos_condition = re.compile(regrex)

    for content in contents:
        clean_content = re.sub('(S|s)peech (R|r)ecognition', '', content)
        nouns = []
        for word,pos in nltk.pos_tag(nltk.word_tokenize(str(clean_content))):
            if pos_condition.match(pos):
#                print word,pos
                lemm_word = wordnet_lemmatizer.lemmatize(word)
                nouns.append(str(lemm_word))
#                print lemm_word
        string = ' '.join(nouns)
        processed_contents.append(string)
#        print string
    return processed_contents