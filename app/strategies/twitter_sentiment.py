import tweepy
from textblob import TextBlob
import csv
import sys
import pandas


"""Perform sentiment analysis on twitter
"""


class Twitter_analysis():


	def __init__(self):

		consumer_key=''
		consumer_secret=''

		access_token_key=''
		access_token_secret=''