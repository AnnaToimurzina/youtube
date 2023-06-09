from googleapiclient.discovery import build
import os
import isodate
import datetime

from datetime import timedelta


class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        playlist_response = PlayList.get_service().playlists().list(id=playlist_id, part="contentDetails, snippet", maxResults=50).execute()
        self.title = playlist_response['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/playlist?list=' + self.playlist_id

    def __repr__(self):
        return f"{self.__class__.__name__}, " \
               f"{self.playlist_id}," \
               f"{self.title}, " \
               f"{self.url}"

    def __call__(self, *args, **kwargs):
        pass

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('YT_API_KEY')
        play_list = build('youtube', 'v3', developerKey=api_key)
        return play_list

    @property
    def total_duration(self):
        """возвращает объект класса`datetime.timedelta`с суммарной длительностью плейлиста"""
        time_line = []
        self.get_play_list()

        # Перебираем список длительностей видео
        for video in self.get_play_list():
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            time_line.append(duration)
        # Суммируем длительность видео в плейлисте
        res = sum(time_line, datetime.timedelta())
        return res

    def show_best_video(self):
        """возвращает ссылку на самое популярное видео из плейлиста"""

        # Ищем лучшее видео и делаем ссылку на него
        high_like = 0
        url_video_top = ''
        for i in self.get_play_list():
            like = i['statistics']['likeCount']
            if int(like) > int(high_like):
                high_like = like
                url_video_top = i['id']

        return f'https://youtu.be/{url_video_top}'

    def get_play_list(self):
        playlist_videos = PlayList.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                                      part='contentDetails',
                                                                      maxResults=50).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = PlayList.get_service().videos().list(part='contentDetails,statistics',
                                                              id=','.join(video_ids)
                                                              ).execute()
        return video_response['items']

