# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 22:43:18 2021

@author: DvdMe
"""

import re
import csv
import pandas
import random

#prep jokes
dino=open('C:\\Users\\DvdMe\\Documents\\good_morning_data\\dino.txt', encoding='utf-8').readlines()

list=[bool(re.search("\d+.", line)) for line in dino]

dino_list=[]

for i,line in enumerate(dino):
    if list[i]:
        dino_list.append([re.sub("\n","",x) for x in [re.sub("\d+. ","",line),dino[i+1]]])

with open("C:\\Users\\DvdMe\\Documents\\good_morning_data\\dino2.csv", "w") as file:
    writer=csv.writer(file)
    writer.writerows(dino_list)

pandas.read_csv("C:\\Users\\DvdMe\\Documents\\good_morning_data\\dino2.csv",header=None)



#pick a line from good_morning_messages


def good_morning_data(name):
        dir="C:\\Users\\DvdMe\\Documents\\good_morning_data\\"
        if name=="anna":
            return(dir+"dino2.csv")

def pick_message(name):
    data=pandas.read_csv(good_morning_data(name),header=None,encoding="ISO-8859-1")
    number=random.randint(0,len(data))
    message=data.iloc(number)[0][0]
    try:
        answer=data.iloc(number)[0][0]
