#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 18:46:56 2018

@author: Harry
"""

import re
import pandas as pd
import matplotlib.pyplot as plt

chatHistoryStr = 'InsertYourChatHistoryHere.txt'

# Open the WhatsApp exported txt file containing chat history
with open(chatHistoryStr) as f:
    pieces = [i.strip() for i in f.read().splitlines()]
f.close()

# Use a horrendous regex expression to split each of the lines into time, name
# and then the message text sent
msgDf = pd.DataFrame(re.findall(r'\[(.*?)\]\s*([^:]+):\s*(.*)', 
                               '\n'.join(pieces)),
                    columns=['Time', 'Name', 'Text'])


# Slice off the unwanted characters in date - always the same
msgDf.Time = msgDf.Time.str[:10]

# Convert the time column to a date format as specified
msgDf['Time'] = pd.to_datetime(msgDf['Time'], format='%d/%m/%Y', errors='coerce')

# Drop any rows which have a NAN for time
msgDf = msgDf.dropna(subset = ['Time'])

# Group all the messages by name and count the size 
msgsPerPerson = msgDf.groupby(['Name']).size().reset_index(name = 'count')

# Hack to clean data. Get rid of people added to the chat over time
msgsPerPerson = msgsPerPerson.drop([4,7,9,10]).reset_index()

# Another hack as per above
msgsPerPerson.drop('index', axis=1, inplace=True)

# Group the messages by time, i.e. all messages for one day
msgsPerDayDf = msgDf.groupby(['Time']).size().reset_index(name = 'count')

# Calculate the 7-day rolling average of number of messages
msgsPerDayDf['rollingWeeklyAverage'] = msgsPerDayDf.iloc[:, 1].rolling(window = 7).mean()


# Plot some figures
plt.figure(1)

# Plot the 9 main people in the chat 
msgsPerPerson = msgsPerPerson[:9].sort_values('count', ascending=False)
plt.bar(msgsPerPerson['Name'], msgsPerPerson['count'])
plt.xticks(rotation=90)
plt.ylabel("Total number of messages sent")

plt.figure(2)
# Plot the average number of messages per day
plt.plot(msgsPerDayDf['Time'], msgsPerDayDf['count'])
plt.xticks(rotation = 90)

# Plot the 7 day rolling average
plt.plot(msgsPerDayDf['Time'], msgsPerDayDf['rollingWeeklyAverage'])
