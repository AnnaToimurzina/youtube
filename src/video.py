from googleapiclient.discovery import build
import os


class Video:
    def __init__(self, video_id: str):
        """Экземпляр инициализируется id канала."""
        self.video_id = video_id
        try:
            video_res = Video.get_service().videos().list(part="snippet,statistics,contentDetails,topicDetails", id=video_id).execute()
            self.video_title = video_res['items'][0]['snippet']['title']
            self.view_count = video_res['items'][0]['statistics']['viewCount']
            self.like_count = video_res['items'][0]['statistics']['likeCount']
            self.comment_count = video_res['items'][0]['statistics']['commentCount']
        except:
            self.video_title = None
            self.view_count = None
            self.like_count = None
            self.comment_count = None


    def __repr__(self):
        return f'{self.__class__.__name__}'\
               f'{self.video_id}'\
               f'{self.video_title}'\
               f'{self.like_count}' \
               f'{self.comment_count}'
    
    def __str__(self):
        return f'{self.video_title}'

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.playlist_id = playlist_id
        
    def __repr__(self):
        return f'{self.__class__.__name__}'\
               f'{self.playlist_id}'\
               f'{self.video_id}'\
               f'{self.video_title}'\
               f'{self.like_count}' \
               f'{self.comment_count}'
        
        
    def __str__(self):
        return super().__str__()
    
 
        



