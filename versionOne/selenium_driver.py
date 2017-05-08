# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 17:11:12 2017

@author: user
"""

import logging
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException
import mongodb as mg
import utilities as ut

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger('selenium_driver')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

config = {}
execfile("/home/alfred/Projects/pj0304/configFile.conf", config)

name_database = config['database']
name_collection = config['collection']

def init_driver():
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 5)
    logger.info("WebDriver initiated")
    return driver

def google_search_keywords_news_link(driver, keywords):
    #search news URL using keywords on Google Search Engine
    logger.debug("Loading Google.com")
    driver.get("http://www.google.com")
    logger.info("Google.com loaded!")
    try:
        box = driver.wait.until(EC.presence_of_element_located((By.NAME, "q")))
        button = driver.wait.until(EC.element_to_be_clickable((By.NAME, "btnK")))
        box.send_keys(keywords)
#        logger.debug("Keywords sent!")
        try:
            button.click()
        except ElementNotVisibleException:
            button = driver.wait.until(EC.visibility_of_element_located((By.NAME, "btnG")))
            button.click()
            
        time.sleep(random.randrange(3, 10))  
        news_link = driver.find_element_by_xpath("//a[@class='q qs']").get_attribute("href")
        logger.debug("News link found using selected keywords")
        return news_link
#        print "news_url:", news_url.get_attribute("href")
    except TimeoutException:
        logger.error("Box or Button not found in google.com")
        return False
    
def crawl_newsLinks(driver, news_link):
    
    mongoClient, db = mg.init_mongo(name_database)
    
#    logger.debug("Loading %s", news_link)
    driver.get(news_link)
    logger.debug("URL Loaded!")
    
    time.sleep(random.randrange(5, 10))  
    searchResults = driver.find_elements_by_xpath("//div[@class='g']")
    next_news_link = driver.find_element_by_xpath("//td[@class='b navend'][2]/a").get_attribute("href")
    
    for searchResult in searchResults:
        
        searchData = dict()
        time.sleep(random.randrange(3, 7))  
        
        try:
            searchData['DirectLink'] = searchResult.find_element_by_xpath("./div/div/h3/a").get_attribute("href")
            searchData['Title'] = searchResult.find_element_by_xpath("./div/div/h3/a").text
        except NoSuchElementException:
            logger.error("Unable to find News directlink")
            continue
        
        try:
            date = searchResult.find_element_by_xpath("./div/div/div/span[3]").text
            searchData['Date'] = ut.date_parser(date)
        except NoSuchElementException:
            logger.warn("No date found")
            searchData['Date'] = None 
            
        try:
            summary = searchResult.find_element_by_xpath("./div/div/div[2]").text
            searchData['Summary'] = summary.replace(u"\u2018", "").replace(u"\u2019", "").replace(u"\u201c","").replace(u"\u201d", "").replace('"', "")
        except NoSuchElementException:
            logger.warn("No summary found")
            searchData['Summary'] = None
            
        mg.insert_doc(db, name_collection, searchData)
#        logger.debug("Data: %s \n", searchData)
    return next_news_link