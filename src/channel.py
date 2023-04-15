import os

from googleapiclient.discovery import build

api_key: str = os.getenv('API_KEY_YOUTUBE')

youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

    def print_info(self, channel_id) -> None:
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        print(channel)

    @classmethod
    def get_service(cls):
        """Класс-метод возвращающий объект для работы с YouTube API"""
        channel = youtube.channels().list(id=api_key, part='snippet,statistics').execute()
        return channel

    @staticmethod
    def to_json():
        """Сохраняет в файл значения атрибутов экземпляра Channel"""


vdud = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')

print(vdud.get_service())