import pyautogui
import time
import re
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import winsound
import PIL
import matplotlib
from playsound import playsound
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
    browser = webdriver.Chrome(r"C:\Users\DvdMe\Downloads\chromedriver.exe",options=options)
    browser.get('https://skyscanner.nl/')
    
    time.sleep(5)
    #remove banner
    pyautogui.moveTo(2540,100,0)
    pyautogui.click()
    pyautogui.press("f5")
    time.sleep(5)
    #accept cookies
    pyautogui.moveTo(1750,1250,1)
    pyautogui.click()
    time.sleep(1)
    #vliegvelden in de buurt
    pyautogui.moveTo(750,510+5,0)
    pyautogui.click()
    time.sleep(1)
    #enkele reis
    pyautogui.moveTo(900,410+10,0)
    pyautogui.click()
    time.sleep(1)
    #Van
    pyautogui.moveTo(750,460+10,0)
    pyautogui.click()
    time.sleep(1)
    pyautogui.write(van)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    #Naar
    pyautogui.moveTo(1100,460+10,0)
    pyautogui.click()
    pyautogui.write(naar)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    #tickets zoeken
    pyautogui.moveTo(1750,515+10,0)
    pyautogui.click()
    time.sleep(10)
    soup=str(bs(browser.page_source,'html.parser'))
    seconds=0
    while True:
        #BS
        soup=str(bs(browser.page_source,'html.parser'))
        if re.search("You need to enable JavaScript to run this app.",soup):
            seconds=1
            playsound(r"C:\Users\DvdMe\Downloads\2022-02-25-14-40-41-AudioTrimmer.mp3")
            pyautogui.moveTo(1200,600,1)
            pyautogui.mouseDown()
            time1=0
            while time1<30:
                image=pyautogui.screenshot()
                if image.getpixel((1425,600))!=(255,255,255):
                    time.sleep(0.5)
                    pyautogui.mouseUp()
                    time.sleep(10)
                    if image.getpixel((1425,600))!=(255,255,255):
                        pyautogui.press("f5")
                        time.sleep(3)
                        break
                time.sleep(0.1)
                time1=time1+0.1
        else:
            break
    if seconds>0:
        startup_skyscanner(van,naar)

def find_prices(van,naar):
    global browser
    global bigdf
    global flag
    
    while True:
        #put away any trash
        pyautogui.moveTo(2200,300,1)
        pyautogui.click()
        #move to cheapest
        pyautogui.moveTo(1400,300,1)
        pyautogui.click()
        pyautogui.moveTo(1400,360,1)
        pyautogui.click()
        seconds=0
        flag=1
        while True:
            time1=0
            #BS
            flag=2
            soup=str(bs(browser.page_source,'html.parser'))
            if re.search("\\d{1,} resultaten",soup):
                break
            elif re.search("You need to enable JavaScript to run this app.",soup):
                flag=3
                playsound(r"C:\Users\DvdMe\Downloads\2022-02-25-14-40-41-AudioTrimmer.mp3")
                time.sleep(5)
                if seconds==1: 
                    pyautogui.moveTo(1200,600,1)
                    seconds=0
                elif seconds==0:
                    pyautogui.moveTo(1300,600,1)
                    seconds=1
                pyautogui.mouseDown()
                while time1<30:
                    flag=4
                    image=pyautogui.screenshot()
                    if image.getpixel((1425,600))!=(255,255,255):
                        flag=4.1
                        time.sleep(0.5)
                        pyautogui.mouseUp()
                        playsound(r"C:\Users\DvdMe\Downloads\2022-02-25-14-40-41-AudioTrimmer.mp3")
                        time.sleep(30)
                        soup=str(bs(browser.page_source,'html.parser'))
                        if re.search("\\d{1,} resultaten",soup):
                                break
                        elif image.getpixel((1425,600))!=(255,255,255):
                            pyautogui.press("f5")
                            time.sleep(3)
                            break
                    time.sleep(0.1)
                    time1=time1+0.1
            else:
                time.sleep(1)
        flag=5
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
            bigdf[3]=van
            bigdf[4]=naar
        print(bigdf)
        bigdf.to_csv(r"C:\Users\DvdMe\Documents\skyscanner.csv",index=False)
        pyautogui.moveTo(1475,200,1)
        pyautogui.click()
        time.sleep(4)
        if date[-3:]=="jun":
            break





try:
    del bigdf
except:
    pass

combinations=list(pd.read_excel(r"C:\Users\DvdMe\Downloads\flights.xlsx",header=None).dropna().to_records(index=False))

for combination in combinations:
    print(combination)
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

