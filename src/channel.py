import json
import os
# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        channel = Channel.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
        self.channel_id = channel_id
        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.url = channel['items'][0]['snippet']['thumbnails']["default"]['url']
        self.subscriberCount = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.viewCount = channel['items'][0]['statistics']['viewCount']

    def __str__(self) -> str:
        return f"{self.title} ({self.url})"

    def __add__(self, highload):
        return int(self.subscriberCount) + int(highload.subscriberCount)

    def __sub__(self, highload):
        return int(self.subscriberCount) - int(highload.subscriberCount)

    def __gt__(self, highload):
        return self.subscriberCount > highload.subscriberCount

    def __ge__(self, highload):
        return self.subscriberCount >= highload.subscriberCount

    def __lt__(self, highload):
        return self.subscriberCount < highload.subscriberCount

    def __le__(self, highload):
        return self.subscriberCount <= highload.subscriberCount

    def __eq__(self, highload):
        return self.subscriberCount == highload.subscriberCount

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()

        '''преобразование объекта channel в формат JSON, и сохраняем результат в переменной info'''
        info = json.dumps(channel, indent=2, ensure_ascii=False)
        print(info)

    @classmethod
    def get_service(cls):
        '''метод возвращает объект для работы с YouTube API'''
        api_key: str = os.getenv('YT_API_KEY')

        '''создаем объект object_get, который может выполнять запросы к YouTube API'''
        object_get = build('youtube', 'v3', developerKey=api_key)
        return object_get

    def to_json(self, file):
        channel_data = {
            'id': self.channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriberCount': self.subscriberCount,
            'video_count': self.video_count,
            'viewCount': self.viewCount,}

        with open(file, 'w', encoding='utf-8') as f:
            json.dump(channel_data, f, indent=2, ensure_ascii=False)


