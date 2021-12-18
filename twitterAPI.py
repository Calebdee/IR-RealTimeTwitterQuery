from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import StreamListener
from tweepy import Stream
import json
import pandas as pd
import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import matplotlib.pyplot as plt
import nltk
from nltk.stem import LancasterStemmer
import pickle


import twitter_credentials

def main():
	fetched_tweets_filename = "tweets.json"
	listener = TwitterListener(fetched_tweets_filename, 1000)
	auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_KEY_SECRET)
	auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

	# with open(fetched_tweets_filename, 'w') as tf:
	# 	tf.write("{\n\t\"tweets\": [")
	stream = Stream(auth, listener)
	stream.sample(languages=["en"])
	# with open(fetched_tweets_filename, 'a') as tf:
	# 	tf.write("\t]\n}")
	print("Pulled tweets, building corpus")

class TwitterListener(StreamListener):
	"""
	This is a basic listener class that just prints received tweets to stdout
	"""
	def __init__(self, fetched_tweets_filename, limit):
		self.fetched_tweets_filename = fetched_tweets_filename
		self.counter = 0
		self.limit = limit
		self.tweets = []

	def on_data(self, data):
		try:
			tweet = json.loads(data)
			twt = Tweet(tweet['id'], tweet['text'], tweet['created_at'], tweet['user']['profile_image_url'])
			self.tweets.append(twt)
			# with open(self.fetched_tweets_filename, 'a') as tf:
			# 	tf.write(data)
			self.counter += 1
			if (self.counter % 500 == 0):
				print(str(self.counter) + " Tweets Pulled")
			if self.counter < self.limit:
				return True
			else:
				stream.disconnect()
				return True
		except BaseException as e:
			print("Error on data: %s" % str(e))
			return True

	def on_error(self, status):
		if status == 420:
			return False
		print(status)

class Tweet():
	def __init__(self, user, text, time, profile_pic):
		self.user = user
		self.text = text
		self.time =  time
		self.pic = profile_pic


class CorpusBuilder():
	def  __init__(self, tweets):
		self.tweets = tweets
		self.corpus = []
		self.inverted_index = {}
		stop_words = self.prepareStop()
		lemma = nltk.wordnet.WordNetLemmatizer()
		for i in range(len(tweets)):
			tokens = word_tokenize(tweets[i].text)
			for tok in tokens:
				tok = lemma.lemmatize(tok).lower()
				if tok not in stop_words:
					if tok in self.inverted_index:
						if i not in self.inverted_index[tok]:
							self.inverted_index[tok].append(i)
					else:
						self.inverted_index[tok] = [i]


		with open('invert_index.pickle', 'wb') as handle:
			pickle.dump(self.inverted_index, handle, protocol=pickle.HIGHEST_PROTOCOL)
		with open('tweet_corpus.pickle', 'wb') as handle:
			pickle.dump(self.tweets, handle, protocol=pickle.HIGHEST_PROTOCOL)

	def prepareStop(self):
		import ssl

		try:
		    _create_unverified_https_context = ssl._create_unverified_context
		except AttributeError:
		    pass
		else:
		    ssl._create_default_https_context = _create_unverified_https_context

		nltk.download('stopwords')
		nltk.download('punkt')
		nltk.download('wordnet')
		stop_words = stopwords.words('english')
		stop_words.append(':')
		stop_words.append('#')
		stop_words.append('@')
		stop_words.append(',')
		stop_words.append('.')
		stop_words.append('https')
		stop_words.append('i')
		stop_words.append('\'')
		stop_words.append('\'s')
		stop_words.append('the')
		stop_words.append('`')
		stop_words.append('\"')
		stop_words.append('?')
		stop_words.append('!')
		stop_words.append('i')
		stop_words.append('’')
		stop_words.append('the')
		stop_words.append('”')
		stop_words.append('“')
		stop_words.append('``')
		stop_words.append('the')
		stop_words.append('it')
		stop_words.append('a')
		stop_words.append(';')
		stop_words.append('RT')
		stop_words.append('rt')
		stop_words.append('co')
		stop_words.append('CO')
		return stop_words
			
		

if __name__ == "__main__":
	fetched_tweets_filename = "tweets.json"
	listener = TwitterListener(fetched_tweets_filename, 50000)
	auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_KEY_SECRET)
	auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

	with open(fetched_tweets_filename, 'w') as tf:
		tf.write("{\n\t\"tweets\": [")
	stream = Stream(auth, listener)
	stream.sample(languages=["en"])
	with open(fetched_tweets_filename, 'a') as tf:
		tf.write("\t]\n}")
	print(len(listener.tweets))
	print("Pulled tweets, building corpus")
	corpus = CorpusBuilder(listener.tweets)


