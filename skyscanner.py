import pyautogui
import time
import pytesseract
import re
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
'''
time.sleep(1)
#open a new chrome window
pyautogui.keyDown('winleft')
pyautogui.press("r")
pyautogui.keyUp('winleft')
pyautogui.write('chrome')
pyautogui.press("enter")
time.sleep(1)
#open a new incognito window
pyautogui.hotkey("ctrl","shift","n")
#go to skyscanner.com
pyautogui.write('skyscanner.com')
pyautogui.press("enter")
'''


def startup_skyscanner(van,naar):
    global browser
    
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("start-maximized")
    options.add_argument('--disable-blink-features=AutomationControlled')
    browser = webdriver.Chrome("C:\\Users\\DvdMe\\Downloads\\chromedriver.exe",options=options)
    browser.get('https://skyscanner.com/')
    
    time.sleep(3)
    #remove banner
    pyautogui.moveTo(2540,100,1)
    pyautogui.click()
    pyautogui.press("f5")
    time.sleep(3)
    #accept cookies
    pyautogui.moveTo(1750,1250,1)
    pyautogui.click()
    time.sleep(1)
    #vliegvelden in de buurt
    pyautogui.moveTo(750,510,1)
    pyautogui.click()
    time.sleep(1)
    #enkele reis
    pyautogui.moveTo(900,410,1)
    pyautogui.click()
    time.sleep(1)
    #Van
    pyautogui.moveTo(750,460,1)
    pyautogui.click()
    time.sleep(1)
    pyautogui.write(van)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    #Naar
    pyautogui.moveTo(1100,460,1)
    pyautogui.click()
    pyautogui.write(naar)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    #tickets zoeken
    pyautogui.moveTo(1750,515,1)
    pyautogui.click()
    time.sleep(3)

def find_prices(van,naar):
    global browser
    
    while True:
        #move to cheapest
        pyautogui.moveTo(1400,300,1)
        pyautogui.click()
        pyautogui.moveTo(1400,350,1)
        pyautogui.click()
        while True:
            #BS
            soup=str(bs(browser.page_source,'html.parser'))
            if re.search("\\d{1,} resultaten",soup):
                break
            else:
                time.sleep(1)
        times=re.findall("\\d{2}u. \\d{2}",soup)
        prices=re.findall("(?:Aanbevolen|Goedkoopste|Snelste|Gesponsord|aanbieding).*?€ (\d*\.*\d*)",soup)[:len(times)]
        times=list(map(lambda x:int(x[:2])+int(x[-2:])/60,times))
        prices=list(map(lambda x:int(str(x).replace(".","")),prices))
        date=re.findall('value="(\\D{2} \\d{1,} \\D{3})',soup)[0]
        try:
            df=pd.DataFrame([times,prices]).transpose()
            df[2]=date
            df[3]=van
            df[4]=naar
            bigdf=bigdf.append(df)
        except:
            bigdf=pd.DataFrame([times,prices]).transpose()
            bigdf[2]=date
        pyautogui.moveTo(1475,200,1)
        pyautogui.click()
        time.sleep(2)
        if date[-3:]=="jun":
            break





try:
    del bigdf
except:
    pass

combinations=list(pd.read_excel(r"C:\Users\DvdMe\Documents\flights.xlsx",header=None).dropna().to_records(index=False))

for combination in combinations:
    startup_skyscanner(*combination)
    find_prices(*combination)
    browser.quit()
    




'''
#Tesseract action
pytesseract.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
while True:
    #take screenshot
    im=pyautogui.screenshot()
    text=pytesseract.image_to_string(im)
    if re.search("resuttaten",text):
        break
'''