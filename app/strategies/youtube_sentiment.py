from apiclient.discovery import build
import pandas as pd
import time

"""Perform sentiment analysis on youtube
"""

class YoutubeAnalysis():

	def __init__(self):


		DEVELOPER_KEY = ""
		YOTUBE_API_SERVICE_NAME = ""
		YOTUBE_API_VERSION = ""

		youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

	def get_videos_FromChannel(youtube, channelId,order):
		search_response = youtube.search().list(
				channelId=channelId,
				type="video",
				part="id,snippet",
				maxResults=50,
				order=orrder

			).execute()

		return search_response.get("items",[])

	def get_comment_threads(youtube,videos):
		tempComments = []
		for videos in videos:
			time.sleep(1.0)
			print(video["snippet"]["title"])
			results = youtube.commentThreads().list(
				part="snippet",
				videoId = video["id"]["videoId"],
				textFormat="plainText",
				maxResults=20,
				order="relevance"

				).execute()

			for item in resulsts["items"]:
				comment = item["snippet"]["topLevelComment"]
				tempComment = dict(videoId=video["id"]["video"], videoName=video["snippet"]["title"],nbrReplies = item["snippet"]["totalReplyCount"],author= comment["snippet"]["authorDisplayName"],likes = comment["snippet"]["likeCount"],publishedAt=comment["snippet"]["publishedAt"],text = comment["snippet"]["textDisplay"].encode('utf-8').strip())
				tempComments.append(tempComment)

		return tempComments


	def getVideoInfos(videos):
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


