## Multi Campus Django Project

Subject : Make Your Own Playlist with Youtube



### One Sound

YouTube에서 음악들을 저장해서 나만의 플레이 리스트를 만들 수 있는 사이트입니다.

url에서 시작지점과 끝지점을 지정해서 원하는 음악을 mp3 파일로 저장하고, 

저장된 음악을 검색할 수 있습니다.



### UI

👉 메인 페이지(1)

![image-20210122143600269](./imges/image-20210122143600269.png)

👉 메인 페이지(2) - 최근 추가한 노래정보

![image-20210122143902845](./imges/image-20210122143902845.png)

👉 메인 페이지(3) - 최근 추가한 플레이리스트

![image-20210122144036444](./imges/image-20210122144036444.png)



👉Search 페이지(1) - 제목 및 가수 검색

![image-20210122144241840](./imges/image-20210122144241840.png)

![image-20210122144349376](./imges/image-20210122144349376.png)

👉Search 페이지(2) - 장르 및 태그로 검색

![image-20210122144431690](./imges/image-20210122144431690.png)

![image-20210122144539284](./imges/image-20210122144539284.png)



### 사용 기술 및 환경

Django, MariaDB, ElasticSearch, Requests, BeautifulSoup, FFmpeg

영상처리를 위한 Python 라이브러리 : youtube-dl, pydub, pillow



### 기술 설명

#### 추천 url 및 가수 이미지 크롤링

![image-20210122142556570](./imges/image-20210122142556570.png)

#### Elastic Search

👉 DB의 SQL문을 활용하지 않고 엘라스틱을 사용한 이유

관계형 데이터베이스는 단순 텍스트 매칭에 대한 검색만을 제공

분산 처리를 통해 거의 실시간에 가까운 데이터 검색 가능

대량의 비정형 데이터 보관 및 검색 가능

전문검색 - 전체를 색인하여 특정 단어가 포함된 문서를 검색하는 것이 가능



### 프로젝트 DB

![erd](./imges/erd.png)



#### (음악 저장 및 검색) 실행영상

<video src="./imges/123.mp4"></video>


