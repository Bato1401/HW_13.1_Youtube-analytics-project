import json

from src.channel import youtube


class Video:
    """Класс создает экземпляр с реальными атрибутами видео с ютуб-канала"""

    def __init__(self, video_id):
        self.video_id = video_id
        self.video_title: str = self.get_info_video()['items'][0]['snippet']['title']
        self.view_count: int = self.get_info_video()['items'][0]['statistics']['viewCount']
        self.like_count: int = self.get_info_video()['items'][0]['statistics']['likeCount']
        self.comment_count: int = self.get_info_video()['items'][0]['statistics']['commentCount']

    def get_info_video(self) -> None:
        """Получает данные по play-листам канала"""
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self.video_id
                                               ).execute()
        return video_response

    def __str__(self):
        return self.video_title

    def __repr__(self):
        return f'Видео id - {self.video_id},\n' \
               f'Название видео - {self.video_title},\n' \
               f'Количество просмотров - {self.view_count},\n' \
               f'Количество лайков - {self.like_count},\n' \
               f'Количество комментариев - {self.comment_count}.'


class PLVideo(Video):
    """Класс получения id плей-листа с ютуб-канала"""

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id  # id плейлиста

    def get_playlist_id(self):
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        return playlist_videos

    def __repr__(self):
        return f'Видео id - {self.video_id},\n' \
               f'Название видео - {self.video_title},\n' \
               f'Количество просмотров - {self.view_count},\n' \
               f'Количество лайков - {self.like_count},\n' \
               f'Количество комментариев - {self.comment_count},\n' \
               f'id плейлиста - {self.playlist_id}.'
