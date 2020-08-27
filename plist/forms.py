from django import forms
from .models import Song, Playlist
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['song_title', 'song_artist', 'song_url']
        widgets = {
            'song_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '영어이름만 저장 가능'}),
            'song_artist': forms.TextInput(attrs={'class': 'form-control'}),
            'song_url': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'song_title': '노래 제목',
            'song_artist': '가수',
            'song_url': 'Youtube URL',
        }


class SongSliceForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ('song_title','song_artist','song_url','song_genre'\
                  ,'song_tag','song_start','song_end','song_detail',)
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
            ('', 'Select Tag'),
            ("0", "탈주"),
            ("1", "비오는날"),
            ("2", "노동요"),
            ("3", "심신안정,ASMR"),
            ("4", "현실도피"),
            ("5", "에러뜰때"),
            ("6", "드라이브"),
        )
        widgets = {
            'song_genre': forms.Select(choices=GENRE_CHOICES, attrs={'class': 'form-control'}),
            'song_title': forms.TextInput(attrs={'class': 'form-control','readonly':'readonly'}),
            'song_artist': forms.TextInput(attrs={'class': 'form-control','readonly':'readonly'}),
            'song_url': forms.TextInput(attrs={'class': 'form-control','readonly':'readonly'}),
            'song_tag': forms.Select(choices=TAG_CHOICES, attrs={'class': 'form-control'}),
            'song_start': forms.TextInput(attrs={'class': 'form-control'}),
            'song_end': forms.TextInput(attrs={'class': 'form-control'}),
            'song_detail': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'song_title': '노래 제목',
            'song_artist': '가수',
            'song_url': 'Youtube URL',
            'song_genre': '장르',
            'song_tag': '노래 태그',
            'song_start': '시작시간',
            'song_end': '종료시간',
            'song_detail': '노래 상세 정보'
        }