# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 22:43:18 2021

@author: DvdMe
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from datetime import timedelta
import time
import pandas
import random
'''

#prep jokes
dino=open('C:\\Users\\DvdMe\\Documents\\good_morning_data\\dino.txt', encoding='utf-8').readlines()

list=[bool(re.search("\d+.", line)) for line in dino]

dino_list=[]

for i,line in enumerate(dino):
    if list[i]:
        dino_list.append([re.sub("\n","",x) for x in [re.sub("\d+. ","",line),dino[i+1]]])

with open("C:\\Users\\DvdMe\\Documents\\good_morning_data\\pankie.csv", "w") as file:
    writer=csv.writer(file)
    writer.writerows(pankie)

pandas.read_csv("C:\\Users\\DvdMe\\Documents\\good_morning_data\\dino2.csv",header=None, encoding='cp1252')

'''

#pick a line from good_morning_messages
def good_morning_data(name):
        dir="C:\\Users\\DvdMe\\Documents\\good_morning_data\\"
        if name=="anna weber":
            return(dir+"dino2.csv")
        elif name=="kili prive":
            return(dir+"kiliR.csv")
        elif name=="anke":
            return(dir+"pankie.csv")

def pick_message(name):
    data=pandas.read_csv(good_morning_data(name),header=None, encoding='cp1252',na_values="")
    number=random.randint(1,len(data))-1
    message=data.iloc[number,0]
    try:
        answer=data.iloc[number,1]
    except:
        answer=""
    data=data.drop(number)
    data.to_csv(good_morning_data(name),header=None, encoding='cp1252',index=False)
    return(message,answer)

def custom_message(name):
    if name=="anna weber":
        custom_message=["Goooood morning Anna! :ma u'\ue007",
                 "I hope you sleepy slept well!"]
    elif name=="jasper prijs":
        custom_message=["Goede morgen Jasso! :ma u'\ue007",
                 "Hier heb je :choco u'\ue007!"]
    else:
        custom_message=""
    return(custom_message)

def delay_time(name):
    global delays
    if name=="anna weber":
        delay=5
    elif name=="kili prive":
        delay=60*3
    elif name=="anke":
        delay=60*3
    #delay=0.1
    delays[name]=delay
    return(delay)

def nick_name(name):
    if name=="anna weber":
        return("Anna")
    elif name=="farah":
        return("Farah")
    elif name=="kili prive":
        return("Kili")
    elif name=="chantal de leest":
        return("Chanti")
    elif name=="freddy":
        return("Freddy")
    elif name=="anke":
        return("Panki-Wan")
    elif name=="jasper prijs":
        return("Jasso")
    else:
        return("stranger")

def complete_message(name):
    global delays
    full_message=custom_message(name)
    try:
        data_message,answer=pick_message(name)
    except:
        data_message,answer="",""
    if full_message=="":
        full_message=["Good morning "+nick_name(name)+"! :ma u'\ue007",
                 "I hope you slept well!"]
    full_message.append(data_message)
    if answer:
        full_message.append("You'll receive the answer in "+str(delay_time(name))+" minutes :)")
        full_answer=["The answer is:",
                         answer,
                         "Have a great "+ datetime.today().strftime("%A") +"! :D"]
    else:
        full_answer=["Have a great "+ datetime.today().strftime("%A") +"! :D"]
    
    return(full_message,full_answer)

def start_whatsappweb():
    global browser
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=C:\\Users\\DvdMe\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\wtsp")
    browser = webdriver.Chrome("C:\\Users\\DvdMe\\Downloads\\chromedriver.exe",options=options)
    browser.get('https://web.whatsapp.com/')
    time.sleep(20)

def go_to(name):
    global browser
    browser.find_element_by_css_selector("[data-tab='3']").clear()
    browser.find_element_by_css_selector("[data-tab='3']").send_keys(name)
    browser.find_element_by_css_selector("[data-tab='3']").send_keys(Keys.RETURN)

def assign_message(names):
    global messages
    global answers
    for name in names:
        messages[name],answers[name]=complete_message(name)
    
def reset_vars():
    global messages
    global answers
    global delays
    messages={}
    answers={}
    delays={}
    
def online():
    try:
        browser.find_element_by_xpath("//*[contains(text(),'online')]")
    except:
        return(False)
    else:
        return(True)

def send_message(name,msg):
    global messages
    global answers
    global browser
    if msg=="message":
        to_send=messages[name]
    elif msg=="answer":
        to_send=answers[name]
    browser.find_element_by_css_selector("[data-tab='9'][contenteditable='true']").clear()
    time.sleep(1)
    for message in to_send:
        browser.find_element_by_css_selector("[data-tab='9'][contenteditable='true']").send_keys(message)
        browser.find_element_by_css_selector("[data-tab='9'][contenteditable='true']").send_keys(Keys.SHIFT,Keys.RETURN)
    time.sleep(1)
    browser.find_element_by_css_selector("[data-tab='9'][contenteditable='true']").send_keys(Keys.RETURN)
    time.sleep(1)
    print("sent "+msg+" to "+name)

names=["anna weber","kili prive","jasper prijs","anke","freddy"]#,"farah","chantal de leest"]
today=datetime.today().day-1
done=False
sent_messages=0
browser_open=False
while True:
    time.sleep(1)
    if datetime.now().hour>=5 and datetime.now().hour<12 and (not done or datetime.today().day!=today) and sent_messages<20:
        if datetime.today().day!=today:
            sent_messages=0
            today=datetime.today().day
            reset_vars()
            assign_message(names)
            start_whatsappweb()
            done=False
            browser_open=True
        if not all(value == False for value in answers.values()):
            for name in names:
                if messages[name]:
                    #go_to("Me!")
                    go_to(name)
                    if online():
                        send_message(name,"message")
                        sent_messages=sent_messages+1
                        messages[name]=False
                        try:
                            delays[name]=datetime.now()+timedelta(minutes=delay_time(name))
                        except:
                            delays[name]=datetime.now()
                elif not messages[name] and answers[name] and delays[name]<datetime.now():
                    #go_to("Me!")
                    go_to(name)
                    send_message(name,"answer")
                    sent_messages=sent_messages+1
                    answers[name]=False
        else:
            done=True
            print("Sent all messages and answers")
    else:
        if browser_open:
            browser.quit()
            print("quit the browser")
            browser_open=False



