'''
Analyse text sentiment
'''
from textblob import TextBlob
import structlog

class TextSentiment():
	def __init__(self):
		self.logger = structlog.get_logger()


	def extract_symbols(self,text,symbol_name,name_symbol):
		"""Return trading symbols of cryptocurrencies in text in format (symbol, name) e.g. ("BTC", "bitcoin")"""
		symbols = set()
		ignore_tags = ["DT"]
		words = [w[0].lower() for w in TextBlob(text).tags if w[1] not in ignore_tags]
		for word in words:
			if word.upper() in symbol_name:
				symbols.add((word.upper(), symbol_name[word.upper()]))
				print(f'Found symbol: {word.upper()}')
			elif word.lower() in name_symbol:
				symbols.add((name_symbol[word.lower()], word.lower()))   
				print(f'Found symbol: {name_symbol[word]}')

		return symbols

	def get_sentiment_analysis(self,text, coins):
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

	def get_verdict(self,sentiment, overall):
		"""Use the result from get_sentiment_analysis to determine which coins to buy and
		return an array of coin symbols e.g. ["XVG", "DGB"]"""
		to_buy = [x for x in sentiment.keys() if sentiment[x] >= 0]
		if overall >= 0:
			# Filter out large coins (ideally take out coins in top 10)
			to_buy = [x for x in to_buy if x[0] not in ["BTC", "LTC", "ETH"]]
			return to_buy
		else:
			return []
