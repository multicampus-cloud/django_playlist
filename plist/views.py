from .forms import SongForm
from .models import Song
from .download import download_video_and_subtitle
from .slice import find_sec, song_slice

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth import views, models, login, authenticate
from .forms import UserForm, LoginForm


class UserCreateView(CreateView):
    form_class = UserForm
    template_name = 'registration/signup.html'
    success_url = "/"


# 로그인 페이지
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('plist.index.html')
        else:
            return HttpResponse('로그인 실패. 다시 시도해보세요')
    else:
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            # login(request, new_user)
            return redirect('index')
    else:
        form = UserForm()
        return render(request, 'registration/signup.html', {'form': form})


# new song 만들기
def song_new(request):
    print('song_new')
    if request.method == "POST":
        form = SongForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)

            # 파일뽑아내는 작업
            download_video_and_subtitle(form.cleaned_data['song_url'], form.cleaned_data['song_title'])
            
            # 파일 자르는 작업
            song_slice(form.cleaned_data['song_title'],form.cleaned_data['song_start'],form.cleaned_data['song_end'])

            song = Song.objects.create(song_title=form.cleaned_data['song_title'],\
                                       song_artist=form.cleaned_data['song_artist'], \
                                       song_url=form.cleaned_data['song_url'],
                                       song_genre=form.cleaned_data['song_genre'], \
                                       song_tag=form.cleaned_data['song_tag'], \
                                       song_detail=form.cleaned_data['song_detail'],\
                                       )
            return redirect('index')
        else:
            return HttpResponse('문제가 발생했습니다. 다시 시도해 주세요.')
    else:
        form = SongForm()
        return render(request, 'plist/song_new.html', {'form': form})


# 메인 페이지
def index(request):
    return render(request, 'plist/index.html')


# 로그인 페이지
def login(request):
    return render(request, 'plist/login.html')


def album(request):
    return render(request, 'plist/album.html')


def event(request):
    return render(request, 'plist/event.html')


def blog(request):
    return render(request, 'plist/blog.html')


def contact(request):
    return render(request, 'plist/contact.html')


def element(request):
    return render(request, 'plist/element.html')


# mypage 안에 my playlist 가져오기(모든 노래가져오기)
def playlist(request):
    song_list = Song.objects.all()
    print('playlist',song_list)
    return render(request, 'plist/myPage/playlist.html', {'song_list': song_list})
