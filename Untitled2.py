#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
#import requests
import string
import nltk
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from nltk.tokenize import sent_tokenize,word_tokenize

nltk.download('averaged_perceptron_tagger')

df = pd.read_excel('Input1.xlsx')
text_data = []
x = input(str('enter class name : '))
for url in df['URL'] :
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(url)
    try :
        text_data.append(driver.find_element(By.CLASS_NAME , value = x).text)
    except :
        text_data.append('url not valid')

df['text_data'] = text_data
df[df['text_data'] == 'url not valid']
df = df[~(df['text_data'] == 'url not valid')]

list_of_stopwords_files = os.listdir(os.getcwd() + '\\StopWords')
stop_words = []
for file in list_of_stopwords_files :
    path = os.getcwd() + '\\StopWords\\' + file
    with open(path,'r') as f :
        for line in f :
            stop_words.append(line.split('|')[0].rstrip())          

negative_words = []
path = os.getcwd() + '\\MasterDictionary\\negative-words.txt'
with open(path,'r') as f :
    for word in f :
        negative_words.append(word.rstrip())

positive_words = []
path = os.getcwd() + '\\MasterDictionary\\positive-words.txt'
with open(path,'r') as f :
    for word in f :
        positive_words.append(word.rstrip())

def syllable(word):
    word = word.lower()
    count = 0
    vowels = "aeiouy"
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("es") or word.endswith("ed"):
        count -= 1
    if count == 0:
        count += 1
    return count

total_word_count = []
postive_word_count = []
negetive_word_count = []
sentense_count = []
personal_pronouns_count = []
syllable_count = []
complex_word_count = []
character_count = []
for data in df['text_data'] :
    a = data
    a = a.replace('“', '')
    a = a.replace('”', '')
    a = a.replace('’', '\'')
    word_count = 0
    posti = 0
    negti = 0
    pp = 0
    syll = 0
    cwc = 0
    char_count = 0
    for token in sent_tokenize(a):
        for word in word_tokenize(token):
            if nltk.pos_tag(nltk.word_tokenize(word))[-1][-1] == 'PRP' :
                pp += 1
            if word not in stop_words:
                if word not in string.punctuation:
                    word_count += 1
                    char_count += len(word)
                if word in positive_words :
                    posti += 1
                if word in negative_words :
                    negti += 1
                if syllable(word) > 2:
                    cwc += 1 
                syll += syllable(word)
                
    total_word_count.append(word_count)
    postive_word_count.append(posti)
    negetive_word_count.append(negti)
    sentense_count.append(len(sent_tokenize(a))) 
    personal_pronouns_count.append(pp)
    complex_word_count.append(cwc)
    syllable_count.append(syll)
    character_count.append(char_count)
    
df['total_word_count']= total_word_count
df['postive_word_count']= postive_word_count
df['negetive_word_count']= negetive_word_count
df['sentense_count']= sentense_count
df['personal_pronouns_count'] = personal_pronouns_count
df['syllable_count'] = syllable_count
df['complex_word_count'] = complex_word_count
df['character_count'] = character_count

df['polarity_score'] = (df['postive_word_count'] - df['negetive_word_count']) / ((df['postive_word_count'] + df['negetive_word_count']) + 0.000001)
df['subjectivity_score'] = (df['postive_word_count'] - df['negetive_word_count']) / (df['total_word_count'] + 0.000001)
df['avg_words_per_Sent'] = df['total_word_count'] / df['sentense_count']
df['percentage_of_complex_words'] = (df['complex_word_count'] / df['total_word_count']) * 100
df['fog_index'] = 0.4 * (df['avg_words_per_Sent'] + df['percentage_of_complex_words'])
df['syllable_per_word'] = df['syllable_count'] / df['total_word_count']
df['avg_word_length'] = df['character_count']/df['total_word_count']

df = df.drop('text_data',axis = 1)
df.to_csv('final_result.csv')

