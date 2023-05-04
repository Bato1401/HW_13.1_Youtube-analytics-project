import datetime
import isodate

from src.channel import youtube


class MixinPL:
    """Класс для получения информации о плей-листе"""

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id

    def get_info(self):
        """Возвращает информацию о плейлисте."""
        playlist_info = youtube.playlists().list(id=self.playlist_id, part='snippet, contentDetails',
                                                 maxResults=50, ).execute()
        return playlist_info

    def get_playlist_info(self):
        """Возвращает данные по видео-роликам в плейлисте"""
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id, part='contentDetails, snippet',
                                                       maxResults=50, ).execute()
        return playlist_videos

    def get_videos_id(self):
        """Возвращает все id видеороликов из плейлиста"""
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.get_playlist_info()['items']]
        return video_ids


class PlayList(MixinPL):
    """Класс для получения данных по плей-листу"""

    def __init__(self, playlist_id):
        super().__init__(playlist_id)
        self.title = self.get_info()['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/playlist?list=' + self.playlist_id

    @property
    def total_duration(self):
        """Возвращает суммарную длительность плейлиста"""
        total_time = datetime.timedelta(hours=0, minutes=0, seconds=0)  # 0:00:00

        # получить все id видеороликов из плейлиста
        video_ids = self.get_videos_id()

        video_response = youtube.videos().list(part='contentDetails,statistics', id=','.join(video_ids)).execute()

        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_time += duration

        return total_time

    def show_best_video(self):
        """Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""
        url_best_video = None
        likes_list = 0
        videos_ids = self.get_videos_id()

        for video_id in videos_ids:
            video_response = youtube.videos().list(id=video_id,
                                                   part='snippet,statistics,contentDetails,topicDetails',
                                                   ).execute()
            likes = int(video_response['items'][0]['statistics']['likeCount'])

            if likes > likes_list:
                likes_list = likes
                url_best_video = 'https://youtu.be/' + video_id

        return url_best_video
