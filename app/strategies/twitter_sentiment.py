import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob
import csv
import sys
import pandas


"""Perform sentiment analysis on twitter
"""


CONSUMER_KEY = "KdiQRTpbQ12wLXOkG8b3HrQWr"
CONSUMER_SECRET = "4l8FkjJCeaQZYXZ1gLZ90uKgogaA2O7m0PHpkooygTcgtM7x5d"
ACCESS_KEY = "953719068888006658-Deh9Z4RaaFk8b6FRwtiypsQQG9Hhzwi"
ACCESS_SECRET = "mv5Z0lavfRwQuRXcqzTPnjTGy9YsQBl5NnRA6Z5Br0DWL"



class TwitterListener(StreamListener):
	def __init__(self, callback):
		self.callback = callback

	def on_data(self, data):
		tweet_json = json.loads(data)
		try: 
			if tweet_json["user"]["id_str"] in FOLLOW_IDS:
				print(tweet_json["text"])
				self.callback(tweet_json)
		except:
			pass
		
class Twitter:
	def __init__(self, tweet_callback=lambda x, y, z: x):
		self.tweet_callback = tweet_callback
		
		self.listener = TwitterListener(self.handle_tweet)
		
		self.auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		self.auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

		self.stream = Stream(self.auth, self.listener)	
		self.stream.filter(follow=FOLLOW_IDS)
	
	def handle_tweet(self, tweet_json):
		screen_name = tweet_json["user"]["screen_name"]
		id = tweet_json["id_str"]
		text = tweet_json["text"].replace("\\", "")

		# Get media if present
		try:
			urls = [x["media_url"].replace("\\", "") for x in tweet_json["entities"]["media"] if x["type"] == "photo"]
			for url in urls:
				response = requests.get(url)
				img = Image.open(io.BytesIO(response.content))
				# Extract text from image
				img_text = pytesseract.image_to_string(img)
				text += f' . {img_text}'
		except KeyError:
			pass

		link = f'https://twitter.com/{screen_name}/status/{id}'

		try:
			self.tweet_callback(text, screen_name, link)
		except:
			pass


def extract_symbols(text):
	"""Return trading symbols of cryptocurrencies in text in format (symbol, name) e.g. ("BTC", "bitcoin")"""
	symbols = set()
	ignore_tags = ["DT"]
	words = [w[0].lower() for w in TextBlob(text).tags if w[1] not in ignore_tags]
	for word in words:
		if word.upper() in symbol_name:
			symbols.add((word.upper(), symbol_name[word.upper()]))
			# print(f'Found symbol: {word.upper()}')
		elif word.lower() in name_symbol:
			symbols.add((name_symbol[word.lower()], word.lower()))   
			# print(f'Found symbol: {name_symbol[word]}')

	return symbols

def get_sentiment_analysis(text, coins):
	"""Return the sentiment analysis of coins mentioned in text in
	the form of a dictionary that aggregates the sentiment of
	sentences that include each of the coins.
	"""
	sentiment = {}
	blob = TextBlob(text)
	for sentence in blob.sentences:
		lowercase_words = [x.lower() for x in sentence.words]
		for coin in coins:
			if coin[0].lower() in lowercase_words or coin[1].lower() in lowercase_words:
				try:
					sentiment[coin] += sentence.sentiment.polarity
				except:
					sentiment[coin] = sentence.sentiment.polarity
	
	return sentiment, blob.sentiment.polarity

def get_verdict(sentiment, overall):
	"""Use the result from get_sentiment_analysis to determine which coins to buy and
	return an array of coin symbols e.g. ["XVG", "DGB"]"""
	to_buy = [x for x in sentiment.keys() if sentiment[x] >= 0]
	if overall >= 0:
		# Filter out large coins (ideally take out coins in top 10)
		to_buy = [x for x in to_buy if x[0] not in ["BTC", "LTC", "ETH"]]
		return to_buy
	else:
		return []



def analyze(text):
	"""
	1. Extract symbols
	2. Get sentiment analysis
	3. Determine which coins to buy
	"""
	coins = extract_symbols(text)
	sentiment, overall = get_sentiment_analysis(text, coins)
	to_buy = get_verdict(sentiment, overall)

	return to_buy

