#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 09:07:51 2017

@author: alfred
"""

import pandas as pd
from seleniumdriver import SeleniumDriver
from contentscraper import ContentScraper

class WebCrawler(object):
    
    def __init__(self, crawl_contents=True):
        
        self.crawl_contents = crawl_contents

    def crawl(self, search_topic, maxPage=3):
        
        seleniumDriver = SeleniumDriver()
        contentScraper = ContentScraper()
    
        link = seleniumDriver.search_newsLink(search_topic+ " news")
        
        page = 1
        df = pd.DataFrame()
        
        while page <= maxPage:
            print("Scraping Page %s..." % (page))
            page += 1
            link, results = seleniumDriver.crawl_newsLink(link)
            for row in results:
                if self.crawl_contents:
#                    print("Scraping: %s" % (row['URL']))
                    contents = contentScraper.scrap_link_goose(row['URL'])
                    if len(contents) > 0:
                        ascii_replace = contents.encode('ascii', 'replace')
                        ascii_replace = ascii_replace.replace('\n', ' ').replace('?', '')
                        row['Contents'] = ascii_replace
                    else:
                        row['Contents'] = None
                df = df.append(row, ignore_index=True)
    
        seleniumDriver.kill()
        return df