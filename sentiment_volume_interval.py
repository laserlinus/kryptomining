# sentiment_volume_interval
# 2017-11-17
# Linus Roxbergh

import sys
import tweepy
import csv
import time
import re
from datetime import datetime
from textblob import TextBlob

access_token = "920267080586448896-aDeEHaaZ9N9daNe5lydLjVwMEPtgE5o"
access_token_secret = "Vnq9G4SDlZgyBYcJoZi0TesHUJqV8fTu4nDcp70HUIxfQ"
consumer_key = "20clpIFI8RHXvT90IifU8xrws"
consumer_secret = "3cSy77nZ569OfXYNaoJKvFoIPlbet17kVgGrMJsbctKnNh4tCQ"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

start = time.time()
inside_minute = -1
tweets_collected = 0
retweets_collected = 0
total_t_sentiment = 0
total_rt_sentiment = 0

class CustomStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        global total_t_sentiment
        global total_rt_sentiment
        global tweets_collected
        global retweets_collected
        global start
        global timepassed

        tweet = process_tweet(status)
        sentiment = sentiment_tweet(tweet)
        if "rt" not in tweet:
            tweets_collected += 1
            total_t_sentiment += sentiment
        else:
            retweets_collected += 1
            total_rt_sentiment += sentiment

        timestamp = datetime.now()
        timestamp = str(timestamp.strftime('%Y/%m/%d %H:%M'))

        timepassed = time.time() - start
        timepassed = round((timepassed / 60), 0)

        print('Date:',timestamp, 'T_S:',total_t_sentiment,'RT_S:', total_rt_sentiment, 'T_Collect:',tweets_collected,'RT_Collect:', retweets_collected)

        if timepassed >= 1:
            write_data(timestamp,total_t_sentiment,total_rt_sentiment,tweets_collected,retweets_collected)
            start = time.time()

            print("timepassed:",timepassed)
            timepassed = 0
            print("Writing data:")
            print("")
            print(timestamp, total_t_sentiment, total_rt_sentiment, tweets_collected, retweets_collected)
            print("")
            print("Writing data:")
            total_t_sentiment = 0
            total_rt_sentiment = 0
            tweets_collected = 0
            retweets_collected = 0

        #print_elapsed(tweets_collected)


    def on_error(self, status_code):
        print >> sys.stderr, 'Error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout..'
        return True # Don't kill the stream

def write_data(timestamp, total_t_sentiment, total_rt_sentiment, tweets_collected, retweets_collected):
    with open(filename, 'a', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp,total_t_sentiment,total_rt_sentiment,tweets_collected,retweets_collected])
        f.close()

def process_tweet(status):
    tweet = str(status.text.encode('utf-8'))
    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert @username to BLANK
    tweet = re.sub('@[^\s]+','',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    return tweet


def sentiment_tweet(tweet):
    tweet = TextBlob(tweet)
    return(tweet.sentiment.polarity)
    #print("Sentiment Score: ", tweet.sentiment.polarity)

def print_elapsed(tweets_collected):
    global inside_minute
    global keywords
    timepassed = time.time() - start
    timepassed = round(timepassed)
    minute = round((timepassed/60),0)
    if(minute != inside_minute and int(minute) != 0 ):
        tweets_per_hour = (60*tweets_collected)/int(minute)
        print("")
        print("Keywords:",keywords)
        print("Time passed:",int(minute),"minute(s).")
        print("Tweets collected:",tweets_collected)
        print("Tweets per hour rate:",int(tweets_per_hour))
        print("Tweets per day rate:", int(tweets_per_hour*24))
        print("")
        inside_minute = minute

#keywords = ['bcash','#bcash','#bitcoincash','bitcoin cash','bch','#bch','bitcoin cash','flippening','#flippening']
#keywords = ['#ethereum','eth','ethereum','#eth']
keywords = ['#bitcoin','bitcoin','btc','#btc']

today = datetime.now()
filename = str(today.strftime('%Y%m%d'))
comment = 'tweets_btc_volumetest7'
filename+= comment
filename+= '.txt'


# Writing csv titles
def write_titles(filename):
    with open(filename, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(['date','tweet_sentiment','retweet_sentiment','number_tweets','number_retweets'])
            f.close()

def start_stream():
    while True:
        try:
            streamingAPI = tweepy.streaming.Stream(auth, CustomStreamListener())
            streamingAPI.filter(track=keywords, languages=['en'])
        except:
            print("Error: sleeping for 8 seconds")
            time.sleep(8)
            continue

write_titles(filename)
start_stream()

#TODO
# RT: Se till så det verkligen är RT. om tweetet innehåller RT nu så räknas det som retweet
# Volym i csv: Få med volym av tweets i csv
# Se på volym i spansktalande?
