# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 15:31:01 2017

@author: user
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException
 
 
def init_driver():
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 5)
    return driver
 
if __name__ == "__main__":
    
    driver = init_driver()
    
    driver.get("http://www.google.com")
    
    try:
        box = driver.wait.until(EC.presence_of_element_located((By.NAME, "q")))
        button = driver.wait.until(EC.element_to_be_clickable((By.NAME, "btnK")))
        box.send_keys("Deep Learning")
        try:
            button.click()
        except ElementNotVisibleException:
            button = driver.wait.until(EC.visibility_of_element_located((By.NAME, "btnG")))
            button.click()
            
#        searchResults = driver.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "g")))
        print "start sleep"
        time.sleep(5)
        print "end sleep"
        searchResults = driver.find_elements_by_xpath("//div[@class='g']")
        for searchResult in searchResults:
            time.sleep(0.5)
            try:
                directlink = searchResult.find_element_by_xpath("./div/h3/a")
                print "text:", directlink.text
                print "href:", directlink.get_attribute("href")
            except NoSuchElementException:
                print "No such element!"
                print ""
                continue
            try:
                date = searchResult.find_element_by_xpath("./div/div/div/span/span")
                print "date:", date.text
                print ""
            except NoSuchElementException:
                print "No date found!"
                print ""
                
#        nextButton = driver.wait.until(EC.element_to_be_clickable((By.ID, "pnnext")))
#        nextButton.click()
        
    except TimeoutException:
        print("Box or Button not found in google.com")
#    driver.quit()