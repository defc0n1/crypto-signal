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






