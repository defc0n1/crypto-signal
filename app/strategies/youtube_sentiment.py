from apiclient.discovery import build
import pandas as pd
import time

import bs4,requests,string,json,itertools
from bs4 import BeautifulSoup

import logging


logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

"""Perform sentiment analysis on youtube
"""

class YoutubeAnalysis():

	def __init__(self):


		DEVELOPER_KEY = "AIzaSyDZCSMHobf8xPmmWF1CvqQiwo5wUXc3Bec"
		YOUTUBE_API_SERVICE_NAME = "youtube"
		YOUTUBE_API_VERSION = "v3"

		youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
		

		

	def get_videos_FromChannel(self,youtube,channelId,order):
		search_response = youtube.search().list(
				channelId=channelId,
				type="video",
				part="id,snippet",
				maxResults=50,
				order=order

			).execute()

		return search_response.get("items",[])


	def get_channel_ids(self,channels):
		for channel in channels:
			body = requests.get(channel)
			bodySoup = BeautifulSoup(body.text)
			channelId = bodySoup.find_all({"button"}, )


	def get_comment_threads(self,youtube,videos):
		tempComments = []
		for video in videos:
			time.sleep(1.0)
			#print(video["snippet"]["title"])
			results = youtube.commentThreads().list(
				part="snippet",
				videoId = video["id"]["videoId"],
				textFormat="plainText",
				maxResults=20,
				order="relevance"

				).execute()

			for item in results["items"]:
				comment = item["snippet"]["topLevelComment"]
				tempComment = dict(videoId=video["id"]["videoId"], videoName=video["snippet"]["title"],nbrReplies = item["snippet"]["totalReplyCount"],author = comment["snippet"]["authorDisplayName"],likes = comment["snippet"]["likeCount"],publishedAt=comment["snippet"]["publishedAt"],text = comment["snippet"]["textDisplay"].encode('utf-8').strip())
				tempComments.append(tempComment)

		return tempComments


	def get_video_infos(self,youtube,videos):
		videoList = {}
		for search_result in videos:
			if search_result["id"]["kind"] =="youtube#video":
				videoList[search_result["id"]["videoId"]] = search_result["snippet"]["title"]

		s = ",".join(videoList.keys())
		videos_list_response = youtube.videos().list(id=s,part='id,statistics').execute()
		res = []
		for i in videos_list_response['items']:
			temp_res = dict(v_title = videoList[i['id']])
			temp_res.update(i['statistics'])
			res.append(temp_res)

		data = pd.DataFrame.from_dict(res)
		data['viewCount'] = data['viewCount'].map(lambda x : float(x))
		data['commentCount'] = data['commentCount'].map(lambda x : float(x))
		return data


