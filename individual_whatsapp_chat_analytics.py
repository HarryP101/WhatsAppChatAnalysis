#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 17:28:23 2021

@author: Harry
"""

import re
import pandas as pd
import matplotlib.pyplot as plt

individualChatHistoryStr = "InsertYourChatHistoryHere.txt"

with open(individualChatHistoryStr) as f:
    pieces = [i.strip() for i in f.read().splitlines()]
f.close()

msgsDf = pd.DataFrame(re.findall(r'\[(.*?)\]\s*([^:]+):\s*(.*)', '\n'.join(pieces)),
                      columns=['Time', 'Name', 'Text'])

# Slice off the unwanted characters in date - always the same
msgsDf.Time = msgsDf.Time.str[:10]

msgsDf['Time'] = pd.to_datetime(msgsDf['Time'], format='%d/%m/%Y', errors='coerce')

msgsDf = msgsDf.dropna(subset = ['Time'])

msgsPerPerson = msgsDf.groupby(['Name']).size().reset_index(name = 'count')

msgsPerDayDf = msgsDf.groupby(['Time']).size().reset_index(name = 'count')

avg_per_day = sum(msgsPerDayDf['count'])/len(msgsPerDayDf['count'])

msgsPerDayDf['rollingWeeklyAverage'] = msgsPerDayDf.iloc[:,1].rolling(window=7).mean()

# Find frequency of words
wordFinderRegex = r'\b\w+\b'
wordsList = [re.findall(wordFinderRegex, text) for text in msgsDf['Text']]
flatWordsList = [item.lower() for sublist in wordsList for item in sublist]

# Put words into a dictionary where the value is the frequency of that word
wordFreq = {} 
for item in flatWordsList: 
    if (item in wordFreq): 
        wordFreq[item] += 1
    else: 
        wordFreq[item] = 1
        
# Sort from most frequent to least frequent
sortedWordFreq = sorted(wordFreq.items(), key=lambda x: x[1], reverse=True)
    
Plot some figures
plt.figure(1)
msgsPerPerson = msgsPerPerson[:9].sort_values('count', ascending=False)
plt.bar(msgsPerPerson['Name'], msgsPerPerson['count'])
plt.xticks(rotation=90)
plt.ylabel("Total number of messages sent")

plt.figure(2)
plt.plot(msgsPerDayDf['Time'], msgsPerDayDf['count'])
plt.xticks(rotation = 90)

plt.figure(3)
plt.plot(msgsPerDayDf['Time'], msgsPerDayDf['rollingWeeklyAverage'])
plt.xticks(rotation = 90)
