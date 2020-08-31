import requests
from bs4 import BeautifulSoup

STATIC_THUMBNAIL_PATH = 'plist/static/plist/img/artist/'


def get_thumbnail(song_artist):
    req_header = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
    }

    # song_artist 로 멜론에서 검색하는 url
    url = "https://www.melon.com/search/total/index.htm?q="+song_artist

    html = requests.get(url, headers=req_header).text
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)

    img_tag = soup.select_one('div.d_artist_list img')

    # 이미지 검색 결과 없을 때
    if img_tag is None:
        return False
    # 이미지 검색 결과 있을 때
    else:
        try:
            # 검색 시 나오는 image url
            img_url = img_tag['src']

            if img_url == 'https://cdnimg.melon.co.kr':
                return False
            else:
                # image 파일 저장하기
                with open(STATIC_THUMBNAIL_PATH+song_artist+'.jpg', 'wb') as file:
                    res = requests.get(img_url, headers=req_header)
                    img_data = res.content
                    file.write(img_data)

            return True

        except Exception:
            return False


if __name__ == "__main__":
    # 잘되는 경우
    print(get_thumbnail('BIBI'))
    # 검색내용 안나오는 경우
    print(get_thumbnail('yejjj'))
