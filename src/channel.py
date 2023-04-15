import os
import json
from googleapiclient.discovery import build

api_key: str = os.getenv('API_KEY_YOUTUBE')

youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.title = self.__get_info()['items'][0]['snippet']['title']  # название канала
        self.description = self.__get_info()['items'][0]['snippet']['description']  # описание канала
        self.url = 'https://www.youtube.com/channel/' + channel_id  # ссылка на канал
        self.subscriberCount = self.__get_info()['items'][0]['statistics']['subscriberCount']  # количество подписчиков
        self.video_count = self.__get_info()['items'][0]['statistics']['videoCount']  # количество видео
        self.viewCount = self.__get_info()['items'][0]['statistics']['viewCount']  # общее количество просмотров

    def __get_info(self):
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels( ).list(id=self.channel_id, part='snippet,statistics').execute()
        return channel

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """Класс-метод возвращающий объект для работы с YouTube API"""
        youtube_obj = build('youtube', 'v3', developerKey=api_key)
        return youtube_obj

    def to_json(self, file_name):
        """Сохраняет в файл значения атрибутов экземпляра Channel"""
        data = {
            'channel_id': self.channel_id,
            'title': self.title,
            'description': self.description,
            'customUrl': self.url,
            'subscriberCount': self.subscriberCount,
            'videoCount': self.video_count,
            'viewCount': self.viewCount
        }

        with open(file_name, 'w') as file:
            json.dump(data, file)

