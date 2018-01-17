"""
Analyse Social Sentiment
"""


from datetime import datetime, timedelta, timezone

import structlog
import pandas

from strategies.youtube_sentiment import YoutubeAnalysis
from strategies.twitter_sentiment import Twitter

class SentimentAnalyzer():

    """Contains all the methods required for analyzing sentiment.
    """
    def __init__(self,exchange_interface):
        self.__exchange_interface = exchange_interface
        self.logger = structlog.get_logger()

    def analyze_twitter_sentiment(self, market_pair):
        print("analyzing twitter sentiment")

    def analyze_yotube_sentiment(self,channels):
        print("analyzing youtube sentiment")