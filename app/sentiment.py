"""
Analyse Social Sentiment
"""


from datetime import datetime, timedelta, timezone

from apiclient.discovery import build

import structlog
import pandas

from strategies.youtube_sentiment import YoutubeAnalysis
#from strategies.twitter_sentiment import Twitter
from strategies.text_sentiment import TextSentiment

class SentimentAnalyzer():

    """Contains all the methods required for analyzing sentiment.
    """
    def __init__(self,exchange_interface):
        self.__exchange_interface = exchange_interface
        self.logger = structlog.get_logger()

    def analyze_twitter_sentiment(self, market_pair):
        print("analyzing twitter sentiment")

    def analyze_youtube_sentiment(self,channels,symbols,symbol_name,name_symbol):
        print("analyzing youtube sentiment")
        youtube_analyzer = YoutubeAnalysis()
        text_sentiment = TextSentiment()


        DEVELOPER_KEY = "AIzaSyDZCSMHobf8xPmmWF1CvqQiwo5wUXc3Bec"
        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
        #print(symbols)
        for channel in channels:
             videos = youtube_analyzer.get_videos_FromChannel(youtube,channel,"viewCount")
             #data = youtube_analyzer.get_video_infos(youtube,videos)
             comments = youtube_analyzer.get_comment_threads(youtube,videos)
             text = ''
             for comment in comments:
             	#print(comment["text"])
             	text += str(comment["text"],'utf-8')
             #print(symbol_name)
             #print(name_symbol)
             coins = text_sentiment.extract_symbols(text,symbol_name,name_symbol)
             sentiment, overall = text_sentiment.get_sentiment_analysis(text, coins)
             to_buy = text_sentiment.get_verdict(sentiment, overall)
             print("BUY:")
             print(to_buy)
             #print(videos)
             ##print(data)
             #print(comments)