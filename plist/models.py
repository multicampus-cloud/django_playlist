from django.db import models

GENRE_CHOICES = (
            ('', 'Select Genre'),
            ('0', '가요'),  # First one is the value of select option and second is the displayed value in option
            ('1', 'R&B'),
            ('2', 'POP'),
            ('3', 'JAZZ'),
            ('4', '인디음악'),
            ('5', '댄스'),
            ('6', '랩/힙합'),
            ('7', '기타'),
        )
TAG_CHOICES = (
            ("", "Select Tag"),
            ("0", "탈주"),
            ("1", "비오는날"),
            ("2", "노동요"),
            ("3", "심신안정,ASMR"),
            ("4", "현실도피"),
            ("5", "에러뜰때"),
            ("6", "드라이브"),
        )


class Song(models.Model):
    # song 제목
    song_title = models.CharField(max_length=100)
    # 아티스트
    song_artist = models.CharField(max_length=30)
    # youtube 링크
    song_url = models.CharField(max_length=400)
    # 장르
    song_genre = models.CharField(choices=GENRE_CHOICES, max_length=128)
    # 태그
    song_tag = models.CharField(choices=TAG_CHOICES, max_length=128)
    # 시작 시간
    song_start = models.CharField(max_length=100, null=True)
    # 끝 시간
    song_end = models.CharField(max_length=100, null=True)
    # 이미지 필드
    song_thumbnail = models.ImageField(blank=True, null=True)
    # song_detail
    song_detail = models.TextField(blank=True, null=True)
    # song author (추가한 사용자)
    author = models.ForeignKey('auth.User', on_delete=models.SET_DEFAULT,default=5)  # ForeignKey 는 class



    def __str__(self):
        return self.song_title + '('+self.song_artist+')'


    def indexing(self):
        obj = SongDocument(
        song_title= self.song_title,
        song_artist = self.song_artist,
        song_url = self.song_url,
        song_genre = self.song_genre,
        song_tag = self.song_tag,
        song_detail = self.song_detail,
        )
        obj.save()
        return obj.to_dict(include_meta=True)


class Playlist(models.Model):
    # 작성자
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # ForeignKey 는 class
    # playlist 제목
    play_title = models.CharField(max_length=200)
    # song_list
    play_list = models.CharField(max_length=200)
    # play_detail
    play_detail = models.TextField()

    def __str__(self):
        return self.play_title
