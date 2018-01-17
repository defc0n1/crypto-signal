"""
Analyse Social Sentiment
"""


from datetime import datetime, timedelta, timezone

from apiclient.discovery import build

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

    def analyze_youtube_sentiment(self,channels):
        print("analyzing youtube sentiment")
        youtube_analyzer = YoutubeAnalysis()
        DEVELOPER_KEY = "AIzaSyDZCSMHobf8xPmmWF1CvqQiwo5wUXc3Bec"
        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
        #get list of youtube channels - extract channel id - analyze them all
        videos = youtube_analyzer.get_videos_FromChannel(youtube,"UCLXo7UDZvByw2ixzpQCufnA","viewCount")
        data = youtube_analyzer.get_video_infos(youtube,videos)
        comments = youtube_analyzer.get_comment_threads(youtube,videos)
        print(videos)
        print(data)
        print(comments)