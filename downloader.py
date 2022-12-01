import pytube
from pytube import YouTube, StreamQuery

class Downloader:
    def __init__(self):
        self.ytVideo = None       # Видео с youtube
        self.streamAudio = None   # Аудио с видео youtube
        self.url = ""             # URL видео
        self.filepath = ""        # Путь к аудио

    def get_url(self, url):
        self.url = url

    def downloadAudio(self, url, output_path=None):
        self.ytVideo = YouTube(url)
        self.streamAudio = self.ytVideo.streams.get_audio_only()

        if not output_path:
            self.filepath = self.streamAudio.download(output_path=".\Mus2")
        else:
            self.filepath = self.streamAudio.download(output_path=output_path)