import pytube
from pytube import YouTube, StreamQuery

from typing import Optional

class Downloader:
    def __init__(self):
        self.ytVideo = None       # Видео с youtube
        self.streamAudio = None   # Аудио с видео youtube
        self.url = ""             # URL видео
        self.filepath = ""        # Путь к аудио

    def get_url(self, url: str):
        self.url = url

    def downloadAudio(self, url: str, output_path: Optional[str] = None):
        self.ytVideo = YouTube(url)
        self.streamAudio = self.ytVideo.streams.get_audio_only()

        if not output_path:
            self.filepath = self.streamAudio.download(output_path=".\Mus2")
        else:
            self.filepath = self.streamAudio.download(output_path=output_path)