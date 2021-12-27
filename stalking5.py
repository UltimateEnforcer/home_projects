# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 22:43:18 2021

@author: DvdMe
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from datetime import timedelta
from selenium.webdriver.common.by import By
import time
import pandas
import random
import jellyfish
import re
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

def message_of_the_day():
    global browser
    global anna_msg
    browser.get("https://www.beagreatteacher.com/daily-fun-fact/page/1/")
    time.sleep(10)
    web_text=browser.find_element(By.CLASS_NAME,"content").text
    anna_msg=re.findall("(Random Fact of the Day:\\n.*)\\nJournal Entry",web_text)[0].split("\n")
    if len(anna_msg)<3:
        anna_msg="\n".join(anna_msg)


#pick a line from good_morning_messages
def good_morning_data(name):
        dir="C:\\Users\\DvdMe\\Documents\\good_morning_data\\"
        if name=="anna weber":
            #return(dir+"dino2.csv")
            return(dir+"anna.csv")
        elif name=="kili prive":
            return(dir+"kiliR.csv")
        elif name=="anke":
            return(dir+"pankie.csv")
        elif name=="laurens":
            return(dir+"laurens.csv")

def pick_message(name):
    global anna_msg
    if name=="anna weber":
        try:
            message=anna_msg.copy()
        except:
            message=anna_msg
    else:
        message=[]
    try:
        data=pandas.read_csv(good_morning_data(name),header=None, encoding='cp1252',na_values="")
        number=random.randint(1,len(data))-1
        message.append(data.iloc[number,0])
        try:
            answer=str(data.iloc[number,1])
        except:
            answer=""
        data=data.drop(number)
        data.to_csv(good_morning_data(name),header=None, encoding='cp1252',index=False)
    except:
        answer=""
    return(message,answer)

def custom_message(name):
    if name=="anna weber":
        custom_message=["Goooood morning Anna! :man r'\ue007",
                 "I hope you sleepy slept well!"]
    elif name=="jasper prijs":
        custom_message=["Goede morgen Jasso! :man r'\ue007",
                 "Hier heb je :choco u'\ue007!"]
    elif name=="laurens":
        custom_message=["Goooeddeee morgen Laurens! Hierbij een raadsel:"]
    else:
        custom_message=""
    return(custom_message)

def delay_time(name):
    global delays
    if name=="anna weber":
        delay=""
    elif name=="laurens":
        delay=60*12
    elif name=="kili prive":
        delay=""
    elif name=="anke":
        delay=60*12
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
    elif name=="laurens":
        return("Laurens")
    else:
        return(name)

def complete_message(name):
    global delays
    full_message=custom_message(name)
    try:
        data_message,answer=pick_message(name)
    except:
        data_message,answer="",""
    if full_message=="":
        full_message=["Good morning "+nick_name(name)+"! :man r'\ue007",
                 "I hope you slept well!"]
    full_message.append(data_message)
    if answer:
        #full_message.append("You'll receive the answer in "+str(delay_time(name))+" minutes :)")
        full_message.append("If you are ready to receive the answer, please respond with: 'I know the answer.' in a text message.")
        full_message.append("If you want to guess the answer, please respond with: 'I want to guess: {INSERT GUESS HERE}' in a text message.")
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
    options.add_argument("start-maximized")
    browser = webdriver.Chrome("C:\\Users\\DvdMe\\Downloads\\chromedriver.exe",options=options)
    message_of_the_day()
    browser.get('https://web.whatsapp.com/')
    time.sleep(60)

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
        to_send=[answers[name]]
        if len(to_send)==1:
            to_send=to_send[0]
    browser.find_element_by_css_selector("[data-tab='9'][contenteditable='true']").clear()
    time.sleep(1)
    for message in to_send:
        if name=="anna weber":
            browser.find_element_by_css_selector("[data-tab='9'][contenteditable='true']").send_keys(message)
            browser.find_element_by_css_selector("[data-tab='9'][contenteditable='true']").send_keys(Keys.SHIFT,Keys.RETURN)
            browser.find_element_by_css_selector("[data-tab='9'][contenteditable='true']").send_keys(dinofy(message))
        else:
            browser.find_element_by_css_selector("[data-tab='9'][contenteditable='true']").send_keys(message)
        browser.find_element_by_css_selector("[data-tab='9'][contenteditable='true']").send_keys(Keys.SHIFT,Keys.RETURN)
    time.sleep(1)
    browser.find_element_by_css_selector("[data-tab='9'][contenteditable='true']").send_keys(Keys.RETURN)
    time.sleep(1)
    print("sent "+msg+" to "+name)

def dino(word):
    if word[-2:]=="\n":
        word=word[:-2]
        return("r"+"a"*((len(word)>1)+(len(word)>4)*(len(word)-4))+"w"*min(1,len(word)-3)+"r"*min(1,(len(word)-2))+"\n")
    else:
        return("r"+"a"*((len(word)>1)+(len(word)>4)*(len(word)-4))+"w"*min(1,len(word)-3)+"r"*min(1,(len(word)-2)))

def dinofy(string):
    dino_words=[]
    for word in [word for word in string.split(" ") if len(word)>0]:
        if word[0]!=":" and word[1:2]!="'":
            dino_words.append(dino(word))
        else:
            dino_words.append(word)
    return(" ".join(dino_words))

names=["kili prive","anna weber","freddy","chantal de leest","kiran","joffrey"]#"laurens",]#,"jasper prijs","anke","freddy"]#,"farah"]
today=datetime.today().day-1
done=False
sent_messages=0
browser_open=False
previous_message="asdfasddsagdsgawrfwevcmkjgfhddegf"
last_message="asdfasddsagdsgawrfwevcmkjgfhddegf"
while True:
    time.sleep(0.5)
    if datetime.now().hour>=5 and datetime.now().hour<22 and (not done or datetime.today().day!=today) and sent_messages<50:
        if datetime.today().day!=today:
            sent_messages=0
            today=datetime.today().day
            start_whatsappweb()
            reset_vars()
            assign_message(names)
            done=False
            browser_open=True
        if not all(value == False for value in answers.values()):
            for name in names:
                if messages[name]:
                    #go_to("Me!")
                    try:
                        go_to(name)
                        #pass
                    except:
                        time.sleep(1)
                        next
                    if online():
                        send_message(name,"message")
                        sent_messages=sent_messages+1
                        messages[name]=False
                        try:
                            delays[name]=datetime.now()+timedelta(minutes=delay_time(name))
                        except:
                            send_message(name,"answer")
                            answers[name]=False
                elif not messages[name] and answers[name]:
                    #go_to("Me!")
                    go_to(name)
                    try:
                        last_message=[x.find_elements(By.CLASS_NAME,"selectable-text") for x in browser.find_elements(By.CLASS_NAME,"message-in")][-1][0].text
                    except:
                        print("cannot find a last message")
                    if jellyfish.damerau_levenshtein_distance("I know the answer.",last_message)<3 and last_message!=previous_message:
                        previous_message=last_message
                        send_message(name,"answer")
                        sent_messages=sent_messages+1
                        answers[name]=False
                    elif jellyfish.damerau_levenshtein_distance("I want to guess: ",last_message[:17])==0 and last_message!=previous_message:
                        previous_message=last_message
                        if jellyfish.damerau_levenshtein_distance(answers[name][1].lower(),last_message[17:].lower())==0:
                            browser.find_element_by_css_selector("[data-tab='9'][contenteditable='true']").clear()
                            time.sleep(0.5)
                            browser.find_element_by_css_selector("[data-tab='9'][contenteditable='true']").send_keys("Perfect, this is the right answer!")
                            time.sleep(0.5)
                            browser.find_element_by_css_selector("[data-tab='9'][contenteditable='true']").send_keys(Keys.RETURN)
                            send_message(name,"answer")
                            answers[name]=False
                            sent_messages=sent_messages+1
                        else:
                            browser.find_element_by_css_selector("[data-tab='9'][contenteditable='true']").clear()
                            time.sleep(0.5)
                            browser.find_element_by_css_selector("[data-tab='9'][contenteditable='true']").send_keys("It looks like you dont have the right answer!\n(Though my spelling check is as strict as it can be)\nYou are "+str(jellyfish.damerau_levenshtein_distance(answers[name][1].lower(),last_message[17:].lower()))+" substitutions away")
                            time.sleep(0.5)
                            browser.find_element_by_css_selector("[data-tab='9'][contenteditable='true']").send_keys(Keys.RETURN)
                            sent_messages=sent_messages+1
                        
        else:
            done=True
            print("Sent all messages and answers")
    else:
        if browser_open:
            browser.quit()
            print("quit the browser")
            browser_open=False



