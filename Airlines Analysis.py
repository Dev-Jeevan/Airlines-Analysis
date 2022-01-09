#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup 
import requests 
import csv
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
wnl = WordNetLemmatizer()
stop = set(stopwords.words('english'))

w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
lemmatizer = nltk.stem.WordNetLemmatizer()

def lemmatize(s):
    s = [wnl.lemmatize(word) for word in s]
    return s

url1 = "https://www.airlinequality.com/airline-reviews/flydubai/page/" #FlyDubai
url2 = "https://www.airlinequality.com/airline-reviews/qatar-airways/page/" #QatarAirways
url3 = "https://www.airlinequality.com/airline-reviews/etihad-airways/page/" #Etihad
url4 = "https://www.airlinequality.com/airline-reviews/lufthansa/page/" #Lufthansa
url5 = "https://www.airlinequality.com/airline-reviews/turkish-airlines/page/" #Turkish Airlines
url6 = "https://www.airlinequality.com/airline-reviews/united-airlines/page/" #United Airlines
url7 = "https://www.airlinequality.com/airline-reviews/austrian-airlines/page/" #Austrian Airlines
url8 = "https://www.airlinequality.com/airline-reviews/american-airlines/page/" #American Airlines


reviews = []
for y in range (1,50):
    k = requests.get(url7 + str(y))
    soup = BeautifulSoup(k.text,'html.parser') 
    Reviews = soup.find_all("div", {"class":"text_content"})
    H = soup.find_all("h1",{"itemprop":"name"})

  
    for i in range(len(Reviews)):
        reviews.append(Reviews[i].text)
        reviews

reviews_df = pd.DataFrame(np.array(reviews), columns = ['Reviews'])
reviews_df.head()


# In[2]:


stop_words = stopwords.words('english')
stop_words


# In[3]:


reviews_df['AirLine'] = reviews_df['Reviews'].apply(lambda x: 'AustrianAirlines')
reviews_df


# In[4]:


reviews_df['LowerCased'] = reviews_df['Reviews'].apply(lambda x: ' '.join(word.lower() for word in x.split()))
reviews_df

reviews_df
# In[5]:


reviews_df['PunctuationsRemoved'] = reviews_df['LowerCased'].str.replace('[^|\w\s]','')
reviews_df


# In[6]:


reviews_df['OtherTextsRemoved'] = reviews_df['PunctuationsRemoved'].str.replace('trip verified', '').replace('not verified', '')
reviews_df


# In[7]:


reviews_df['StopWordsRemoved'] = reviews_df['OtherTextsRemoved'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))
reviews_df


# In[8]:


reviews_df['Lemmatized'] = reviews_df['StopWordsRemoved'].apply(lemmatize_text).replace(',' , '')
reviews_df


# In[9]:


pip install textblob


# In[10]:


from textblob import TextBlob


reviews_df['Polarity'] = reviews_df['StopWordsRemoved'].apply(lambda x: TextBlob(x).sentiment[0])
reviews_df


# In[11]:


reviews_df['Sentiment'] = reviews_df['Polarity'].apply(lambda c: 'neutral' if c==0 else 'positive' if c>=-0.01 else 'negative')
reviews_df


# In[12]:


image = []
url = (url7)
r = requests.get(url + str(2))
soup = BeautifulSoup(r.text, 'html.parser')
div = soup.find(class_='logo')
print (div)


# In[13]:


reviews_df['ImgUrl'] = reviews_df['Reviews'].apply(lambda x: 'https://www.airlinequality.com/wp-content/uploads/2015/04/AUSTRIAN_1000.png')
reviews_df


# In[24]:


pip install certifi


# In[25]:


import pymongo
from pymongo import MongoClient
import certifi
ca = certifi.where()

cluster = MongoClient("mongodb+srv://Admin:Mongouser123@cluster0.lplmh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", tlsCAFile=ca)
db  = cluster["Airlines"]
collection = db["AustrianAirlines"]

collection.insert_many(reviews_df.to_dict('records'))


# In[ ]:




