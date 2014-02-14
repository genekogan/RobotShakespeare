import sys
from StringIO import StringIO
import re
import nltk
from nltk.tokenize.punkt import PunktSentenceTokenizer
from random import choice
from nltk.model.ngram import *
import tweepy
import time

# twitter oauth config -- change these to your own twitter account :)
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_KEY_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

# parameters
TRAINING_FILE = 'data/ShakespeareAll.txt'
SLEEP_TIME = 60 * 30
TRY_LIMIT = 50

# todo:
#  perplexity evaluation
#  fix line breaks

def store_output(func, length):
    saved_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    func(length)   # Call function
    sys.stdout = saved_stdout
    return mystdout.getvalue()

def train():
	with open (TRAINING_FILE, "r") as myfile:
	    data = myfile.readlines()
	text = ''
	for d in data:
		text += d
	tokens = nltk.word_tokenize(text)
	nltk_text = nltk.Text(tokens)
	print "finished training model"
	return nltk_text

def pre_process(out):	
	out = re.sub(' \' ', '\'', out)
	out = re.sub(' \'', '\'', out)
	out = re.sub(' , ', ', ', out)
	out = re.sub(' ; ', '; ', out)
	out = re.sub(' : ', ': ', out)	

	# hack: get rid of stage names (capital letters)
	words = out.split(' ')
	for word in words:
		if len(re.compile('[A-Z]').findall(word)) == len(re.compile('[A-Za-z]').findall(word)) and len(word) > 1:
			try:
				out = re.sub(word, '', out)
			except:
				pass
	return out
	
def generate_tweet(nltk_text):
	text = nltk_text.generate
	out = store_output(text, 10000)
	out = PunktSentenceTokenizer().tokenize(out)
	out = out[5:]	# get rid of initial jargon/repetition
	criteria = False
	num_tries = 0
	while not criteria and num_tries <= TRY_LIMIT:
		tweet = choice(out)
		tweet = pre_process(tweet)
		if len(tweet) > 80 and len(tweet) < 140:
			criteria = True
		else:
			num_tries += 1
	if criteria:
		return tweet
	else:
		return None
            
def setup_twitter():
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	twitter = tweepy.API(auth)
	print "setup twitter OAuth"
	return twitter
	
def send_tweet(twitter, tweet):
    success = False
    try:
		print "Attempting TWEET: "+tweet
        twitter.update_status(tweet)
        success = True
		print " => Successfully tweeted:"
    except:
		print " => Tweet failed"
		pass
    return success
	
def main():
    twitter = setup_twitter()
    nltk_text = train()
    while 1:
		tweet = None
		while tweet is None:
			tweet = generate_tweet(nltk_text)
			tweet_result = send_tweet(twitter, tweet)
			if tweet_result:
				print tweet
				time.sleep(SLEEP_TIME)

main()		
