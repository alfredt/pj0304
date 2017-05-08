#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 14:12:50 2017

@author: alfred
"""

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException

import utilities as ut

class SeleniumDriver(object):

    def __init__(self):
        cap = DesiredCapabilities.PHANTOMJS.copy()
        cap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"
        cap["phantomjs.page.settings.loadImages"] = False
        cap["phantomjs.page.settings.webSecurityEnabled"] = False
        service_args = ['--ignore-ssl-errors=true','--ssl-protocol=tlsv1']
        self.driver = webdriver.PhantomJS(desired_capabilities=cap, service_args = service_args)
        self.driver.set_window_size(1366,768)
        self.wait = WebDriverWait(self.driver,30)
    
    def kill(self):
        self.driver.quit()
        
    def search_newsLink(self, keywords):
        #search news URL using keywords on Google Search Engine
        self.driver.get("http://www.google.com")
        try:
            box = self.wait.until(EC.presence_of_element_located((By.NAME, "q")))
            button = self.wait.until(EC.element_to_be_clickable((By.NAME, "btnK")))
            box.send_keys(keywords)
            
            try:
                button.click()
            except ElementNotVisibleException:
                button = self.wait.until(EC.visibility_of_element_located((By.NAME, "btnG")))
                button.click()
                
            self.wait.until(lambda driver:driver.find_element_by_xpath("//a[@class='q qs']"))	
            news_link = self.driver.find_element_by_xpath("//a[@class='q qs']").get_attribute("href")
            return news_link
    #        print "news_url:", news_url.get_attribute("href")
        except TimeoutException:
            print("Box or Button not found in google.com")
            return False
        
    def crawl_newsLink(self, news_link):
        self.driver.get(news_link)
        
        self.wait.until(lambda driver:driver.find_element_by_xpath("//div[@class='g']"))
        searchResults = self.driver.find_elements_by_xpath("//div[@class='g']")
        
        self.wait.until(lambda driver:driver.find_element_by_xpath("//td[@class='b navend'][2]/a"))
        next_news_link = self.driver.find_element_by_xpath("//td[@class='b navend'][2]/a").get_attribute("href")
        
        returnList = list()
    
        for searchResult in searchResults:
            searchData = dict()
            
            try:
                searchData['URL'] = searchResult.find_element_by_xpath("./div/div/h3/a").get_attribute("href")
                searchData['Title'] = searchResult.find_element_by_xpath("./div/div/h3/a").text
            except NoSuchElementException:
                print("Unable to find News directlink")
                continue
            
            try:
                date = searchResult.find_element_by_xpath("./div/div/div/span[3]").text
                searchData['Date'] = ut.date_parser(date)
            except NoSuchElementException:
                print("No date found")
                searchData['Date'] = None 
                
            try:
                summary = searchResult.find_element_by_xpath("./div/div/div[2]").text
                searchData['Summary'] = summary.replace(u"\u2018", "").replace(u"\u2019", "").replace(u"\u201c","").replace(u"\u201d", "").replace('"', "")
            except NoSuchElementException:
                print("No summary found")
                searchData['Summary'] = None
            
            returnList.append(searchData)
            
        return next_news_link, returnList