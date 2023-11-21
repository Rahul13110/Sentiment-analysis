# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 15:02:27 2023

@author: muvva
"""

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import getpass as gp
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from googletrans import Translator  # Import the Translator class
import re

import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

website = 'https://twitter.com/login'
driver = webdriver.Chrome()
driver.get(website)

subject = "#kcr"

# Set up the login
sleep(3)
wait = WebDriverWait(driver, 20)
username = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='text']")))
username.send_keys("rahul171235")
next_button = driver.find_element(By.XPATH, "//span[contains(text(),'Next')]")
next_button.click()

sleep(3)
password = driver.find_element(By.XPATH, "//input[@name= 'password']")
password.send_keys('Rahul@13110')
log_in = driver.find_element(By.XPATH, "//span[contains(text(),'Log in')]")
log_in.click()

# Search item and fetch it
sleep(3)
search_box = driver.find_element(By.XPATH, "//input[@data-testid='SearchBox_Search_Input']")
search_box.send_keys(subject)
search_box.send_keys(Keys.ENTER)

# UserTag = driver.find_element(By.XPATH,"//body/div[@id='react-root']/div[1]/div[1]/div[2]/main[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/section[1]/div[1]/div[1]/div[1]/div[1]/div[1]/article[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/a[1]/div[1]/div[1]/span[1]/span[1]").text
# print(UserTag)

all_tweets = set()
translator = Translator()

while True:
    tweets = driver.find_elements(By.XPATH, "//div[@data-testid='tweetText']")
    for tweet in tweets:
        try:
            tweet_text = tweet.text
            # Translate tweet text to English
            translation = translator.translate(tweet_text, dest='en')
            all_tweets.add(translation.text)
            print(translation.text)
        except selenium.common.exceptions.StaleElementReferenceException:
            # Handle the stale element exception by re-fetching the tweets
            tweets = driver.find_elements(By.XPATH, "//div[@data-testid='tweetText']")
            continue

    driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    sleep(3)

    if len(all_tweets) > 1000:
        break

# Convert the set of translated tweets to a list and then create a DataFrame
all_tweets = list(all_tweets)
df = pd.DataFrame({'KCRTweets': all_tweets})

df.rename(columns={'KCRTweets': 'tweets'}, inplace=True)

# Save the DataFrame to a CSV file
df.to_csv('KCRtwitter_tweets.csv', index=False)

df.head()

df.tail()



df.columns


#breaking the tweet
cleanTweet.split()
stp_words = stopwords.words('english')
print(stp_words)




#cleaning the tweets applying the cleaning on one tweet
one_tweet = df.iloc[4]['tweets']
one_tweet



from textblob import TextBlob
from wordcloud import WordCloud

def TweetCleaning(tweet):
    cleanTweet = re.sub(r"@[a-zA-Z0-9]+","",tweet)
    cleanTweet = re.sub(r"#[a-zA-Z0-9\s]+","",cleanTweet)
    cleanTweet = ' '.join(word for word in cleanTweet.split() if word not in stp_words)
    return cleanTweet

def calPolarity(tweet):
    return TextBlob(tweet).sentiment.polarity

def calSubjectivity(tweet):
    return TextBlob(tweet).sentiment.subjectivity

def segmentation(tweet):
    if tweet > 0:
        return "positive"
    if tweet == 0:
        return "neutral"
    else:
        return "negative"



df['cleanedTweets'] = df['tweets'].apply(TweetCleaning)
df['tPolarity'] = df['cleanedTweets'].apply(calPolarity)
df['tSubjectivity'] = df['cleanedTweets'].apply(calSubjectivity)
df['segmentation'] = df['tPolarity'].apply(segmentation)
df.head()


# # Analysis and Visualization

df.pivot_table(index=['segmentation'],aggfunc={'segmentation':'count'})


# top 3 most positive
df.sort_values(by=['tPolarity'],ascending=False).head(3)


# top 3 most negative
df.sort_values(by=['tPolarity'],ascending=True).head(3)


# 3 neutral
df[df.tPolarity==0]



import matplotlib.pyplot as plt

consolidated = ' '.join(word for word in df['cleanedTweets'])

wordCloud = WordCloud(width=400, height=200, random_state=20, max_font_size=119).generate(consolidated)

plt.imshow(wordCloud, interpolation='bilinear')
plt.axis('off')
plt.show()





import seaborn as sns



df.groupby('segmentation').count()


plt.figure(figsize=(10,5))
sns.set_style("whitegrid")
sns.scatterplot(data=df, x='tPolarity',y='tSubjectivity',s=100,hue='segmentation')


sns.countplot(data=df,x='segmentation')



positive = round(len(df[df.segmentation == 'positive'])/len(df)*100,1)
negative = round(len(df[df.segmentation == 'negative'])/len(df)*100,1)
neutral = round(len(df[df.segmentation == 'neutral'])/len(df)*100,1)

responses = [positive, negative, neutral]
responses

response = {'resp': ['mayWin', 'mayLoose', 'notSure'], 'pct':[positive, negative, neutral]}
pd.DataFrame(response)































































