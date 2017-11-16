# tweetstreamer1
# 2017-10-19
# Linus Roxbergh

import sys
import tweepy
import csv
import time
from datetime import datetime

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

class color:
   BOLD = '\033[1m'
   END = '\033[0m'

class CustomStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        tweet = str(status.text.encode('utf-8'))
        if "RT" not in tweet:
            print(color.BOLD + "*",status.author.screen_name, "", status.created_at, "", tweet+ color.END)
        else:
            print(status.author.screen_name, "", status.created_at, "", tweet)
        global tweets_collected
        tweets_collected += 1
        print_elapsed(tweets_collected)
        # Writing status data
        #print(status)
        with open(filename, 'a', encoding='utf8') as f:
            if "RT" not in tweet:
                writer = csv.writer(f)
                writer.writerow([status.author.screen_name, status.created_at, status.text.encode('utf-8'),'0'])
            else:
                writer = csv.writer(f)
                writer.writerow([status.author.screen_name, status.created_at, status.text.encode('utf-8'), '1'])
            f.close()


    def on_error(self, status_code):
        print >> sys.stderr, 'Error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout..'
        return True # Don't kill the stream


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
comment = 'bcash_tweets'
filename+= comment
filename+= '.txt'


# Writing csv titles
def write_titles(filename):
    with open(filename, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(['Author', 'Date', 'Text','RT'])
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
