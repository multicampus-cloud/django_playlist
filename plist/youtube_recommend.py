import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re


def recommend_song_list(url):

    recommend_list = []

    req_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
    }

    response = requests.get(url, headers=req_headers)

    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # 정규식
    regex_filter = r'title":{"accessibility".*?"commandMetadata":{"webCommandMetadata":{"url":"/watch\?v=.*?"'

    song_list = re.findall(regex_filter, str(soup))

    for song in song_list[:3]:
        recommend = {}
        song = re.sub(
            'title":{"accessibility":{"accessibilityData":{"label":"', '', str(song))
        title = re.split('게시자', str(song))

        sub_link = re.split(
            '"commandMetadata":{"webCommandMetadata":{"url":"', str(song))[-1]
        link = urljoin('https://www.youtube.com', sub_link)

        recommend[title[0]] = link
        recommend_list.append(recommend)

    return recommend_list


if __name__ == '__main__':
    tests = recommend_song_list('https://www.youtube.com/watch?v=Bl4dfyDTXmU')

    for test in tests:
        print(test)
