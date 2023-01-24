import pytube
from pytube import YouTube, StreamQuery
import requests
from bs4 import BeautifulSoup
import json

from typing import Optional

TEMPLATES = ['https://www.youtube.com/results?search_query=', 'https://www.youtube.com']

class Downloader:
    def __init__(self):
        self.ytVideo = None       # Видео с youtube
        self.streamAudio = None   # Аудио с видео youtube
        self.url: str = ""             # URL видео
        self.filepath: str = ""        # Путь к аудио

    def get_url(self, url: str):
        self.url = url

    def downloadAudio(self, url: str, output_path: Optional[str] = None):
        self.ytVideo = YouTube(url)
        self.streamAudio = self.ytVideo.streams.get_audio_only()

        if not output_path:
            self.filepath = self.streamAudio.download(output_path=".\Mus2")
        else:
            self.filepath = self.streamAudio.download(output_path=output_path)

    # Метод для получения страницы с результатами поиска
    def parseSearch(self, title: str):
        info: list[str] = title.split('-')                  # Отделяем исполнителя от названия песни
        track = info[1][1:]                                 # Название песни
        words: list[str] = (info[0] + track).split(' ')
        url_word = ''

        # Преобразуем все слова в запросе к нижнему регистру
        size = len(words)
        for i in range(size):
            words[i] = words[i].lower()

        # Составляем url-адрес страницы результатов поиска
        for word in words:
            url_word += word + '+'
        url_word = url_word[:-1]

        request = TEMPLATES[0] + url_word
        response = requests.get(request, auth=('user', 'pass'))   # Получаем страницу результатов поиска
        return response, track

    # Метод для получения страницы с видео с музыкой
    def parseAudio(self, title: str) -> str:

        # Ищем страницу со списком видео на ютуб с соответствующими названиями песен
        response, track = self.parseSearch(title)
        soup = BeautifulSoup(response.text, 'html.parser')  # Получаем html-код страницы
        root = soup.body                                    # тело html-документа
        tags = root.find_all('script')                      # получаем все тэги <script>
        stroki = list([])

        i = 0
        index = -1

        # В данном цикле ищем самый большой по объему тэг
        for tag in tags:
            stroki.append(str(tag))
            if len(stroki[i]) > 500:
                index = i
                break
            i += 1

        content = str(tags[index].contents[0])  # Получаем содержимое тега script
        content = content[20:-1]
        sp_content = content.split(',')         # Разделяем строку по запятым

        label_spisok = list([])  # Список заголовков, описаний и url полученных видео

        # Находим в цикле информацию о заголовках, описаниях и url полученных видео и заносим их в список
        for elem in sp_content:
            if '"title"' in elem or '"accessibility"' in elem or '"commandMetadata"' in elem:
                label_spisok.append(elem)

        key_spisok = list([])  # Список индексов, по которым можно обратиться к строкам, в которых содержится заголовок видео
        size = len(label_spisok)  # Размер списка заголовков, описаний и url полученных видео
        for i in range(size):
            if '"title"' in label_spisok[i]:  # Если в данной строке содержится заголовок видео,
                key_spisok.append(i)  # то добавляем номер строки в список индексов

        VideoList = dict()  # Список данных о видео
        currentKey = ''
        for i in range(size):  # Проходимся по списку заголовков и данных о видео
            if i in key_spisok:  # Если индекс ссылается на строку с заголовком видео
                currentKey = str(i)
                VideoList[currentKey] = list([])  # Добавляем новый список в общий список
                VideoList[currentKey].append(label_spisok[i])  # И добавляем строку с загловком в подсписок
            else:
                VideoList[currentKey].append(label_spisok[i])  # В противном просто добавляем строку в подсписок

        updatedKeySpisok = list([])
        for key in key_spisok:
            if 'One More Light' in label_spisok[key] and (
                    '[Official Music Video]' in label_spisok[key] or '(Official Audio)' in label_spisok[key]):
                updatedKeySpisok.append(key)

        targetKey = str(updatedKeySpisok[0])
        targetString = ''
        for elem in VideoList[targetKey]:
            if 'watch' in elem:
                targetString = elem
                break

        tagList = targetString.split(':')
        address = ''
        for elem in tagList:
            if 'watch' in elem:
                address = elem            # Находим ссылку на видео
                break

        address = address[1:-1]
        urlFinal = TEMPLATES[1] + address   # Формируем url-адрес видео с песней
        return urlFinal
