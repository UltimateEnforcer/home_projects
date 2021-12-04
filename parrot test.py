# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 22:09:11 2021

@author: DvdMe
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import *
from datetime import datetime
from datetime import timedelta
import time
import pandas
import random
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:\\Users\\DvdMe\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\wtsp")
browser = webdriver.Chrome("C:\\Users\\DvdMe\\Downloads\\chromedriver.exe",options=options)
browser.get('https://web.whatsapp.com/')



browser.find_element_by_css_selector("[data-tab='9'][contenteditable='true']").send_keys("Dirk :parr u'\ue007 activated!")
time.sleep(0.5)
browser.find_element_by_css_selector("[data-tab='9'][contenteditable='true']").send_keys(Keys.RETURN)
last_text=[x.text for x in browser.find_elements(By.CLASS_NAME,"message-in")][-1][:-6]
while True:
    if last_text!=[x.text for x in browser.find_elements(By.CLASS_NAME,"message-in")][-1][:-6]:
        last_text=[x.text for x in browser.find_elements(By.CLASS_NAME,"message-in")][-1][:-6]
        message=last_text
        browser.find_element_by_css_selector("[data-tab='9'][contenteditable='true']").send_keys(message+" :parr u'\ue007")
        time.sleep(0.5)
        browser.find_element_by_css_selector("[data-tab='9'][contenteditable='true']").send_keys(Keys.RETURN)
        print("I sent: \n",message)



#[x.find_elements(By.CLASS_NAME,"selectable-text") for x in browser.find_elements(By.CLASS_NAME,"message-in")][-1][0].text