from .forms import SongForm,UserForm, LoginForm
from .models import Song, Playlist
from .download import download_video_and_subtitle
from .slice import find_sec, song_slice
from .get_artist_thumbnail import get_thumbnail
from .youtube_recommend import recommend_song_list
from .documents import SongDocument

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth import views, models, login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


GENRE_CHOICES = (
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
    ("0", "탈주"),
    ("1", "비오는날"),
    ("2", "노동요"),
    ("3", "심신안정,ASMR"),
    ("4", "현실도피"),
    ("5", "에러뜰때"),
    ("6", "드라이브"),
)


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
@login_required
def song_new(request):
    if request.method == "POST":
        form = SongForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)

            # 파일뽑아내는 작업
            download_video_and_subtitle(form.cleaned_data['song_url'], form.cleaned_data['song_title'])

            # 파일 자르는 작업
            song_slice(form.cleaned_data['song_title'],form.cleaned_data['song_start'],form.cleaned_data['song_end'])

            # 썸네일 만드는 작업
            print(form.cleaned_data['song_artist'])
            verify = get_thumbnail(form.cleaned_data['song_artist'])
            print(verify)
            if verify:
                thumbnail = form.cleaned_data['song_artist']
            else:
                thumbnail = 'default'

            #post = Song.objects.get(pk=3)
            #post.delete()

            # db에 넣기
            song = Song.objects.create(song_title=form.cleaned_data['song_title'],\
                                       song_artist=form.cleaned_data['song_artist'], \
                                       song_url=form.cleaned_data['song_url'],
                                       song_genre=form.cleaned_data['song_genre'], \
                                       song_start=form.cleaned_data['song_start'], \
                                       song_end=form.cleaned_data['song_end'], \
                                       song_tag=form.cleaned_data['song_tag'], \
                                       song_thumbnail=thumbnail,\
                                       song_detail=form.cleaned_data['song_detail'],\
                                       author=request.user,
                                       )

            return redirect('index')
        else:
            return HttpResponse('문제가 발생했습니다. 다시 시도해 주세요.')
    else:
        form = SongForm()
        print("===request.user===")
        print(request.user)
        return render(request, 'plist/song_new.html', {'form': form})


# 특정 song detail 정보 가져오기
def song_detail(request,pk):
    song = get_object_or_404(Song, pk=pk)
    song_tag = TAG_CHOICES[int(song.song_tag)]
    song_genre = GENRE_CHOICES[int(song.song_genre)]
    # 추천 노래 리스트 받아오기
    recommend_list = recommend_song_list(song.song_url)
    # print(recommend_list)
    return render(request, 'plist/song_detail.html', \
                  {'song': song,'genre':song_genre[1], 'tag':song_tag[1],\
                   'recommend_list':recommend_list})


# 메인 페이지
def index(request):
    return render(request, 'plist/index.html')


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


# mypage 안에 my playlist 가져오기(모든 노래가져오기) + playlist 목록 가져오기
@login_required
def playlist(request):
    # 페이지 별로 구분해서 리스트 출력하기
    song_list = Song.objects.filter(author=request.user)
    # song_list 목록에서 한페이지당 2개씩 할당
    paginator = Paginator(song_list, 6)
    # page 받아오기
    page = request.GET.get('page')

    try:
        song_list = paginator.page(page)
    except PageNotAnInteger:
        song_list = paginator.page(1)
    except EmptyPage:
        song_list = paginator.page(paginator.num_pages)

    # 플레이리스트 가져오기
    play_list = Playlist.objects.all()

    return render(request, 'plist/myPage/playlist.html', {'song_list': song_list, 'play_list': play_list})


# 특정 playlist 들어있는 노래목록 가져오기
def play_detail(request, pk):
    play_detail_list = get_object_or_404(Playlist, pk=pk)

    song_list = []
    song_id_list = play_detail_list.play_list.split(',')
    for song_id in song_id_list:
        song = get_object_or_404(Song,pk=song_id)
        song_list.append(song)

    return render(request, 'plist/myPage/play_detail.html', {'play_detail_list': play_detail_list, 'song_list':song_list})


def search_title(request):
    q = request.GET.get('q')
    if q:
        songs = SongDocument.search().query('match',song_title=q)
    else:
        songs = ''
    return render(request, 'plist/title.html',{'songs':songs})


def search_artist(request):
    a = request.GET.get('a')
    if a:
        singer = SongDocument.search().query('match',song_artist=a)
    else:
        singer = ''
    return render(request, 'plist/artist.html', {'singer':singer})


def search_genre(request):

    # return render(request,'plist/genre.html')
    kpops = Song.objects.filter(song_genre='0')
    r_bs = Song.objects.filter(song_genre='1')
    pops = Song.objects.filter(song_genre='2')
    jazzs = Song.objects.filter(song_genre='3')
    indies = Song.objects.filter(song_genre='4')
    dances = Song.objects.filter(song_genre='5')
    hiphops = Song.objects.filter(song_genre='6')
    elses = Song.objects.filter(song_genre='7')
    # a = request.POST.get('pop')
    # if a:
    return render(request, 'plist/genre.html',
                  {'kpops': kpops,
                   'pops': pops,
                   'r_bs': r_bs,
                   'jazzs': jazzs,
                   'indies':indies,
                   'dances': dances,
                   'hiphops':hiphops,
                   'elses': elses,
                   })


def search_tag(request):
    # return render(request,'plist/genre.html')
    tag_0 = Song.objects.filter(song_tag='0')
    tag_1 = Song.objects.filter(song_tag='1')
    tag_2 = Song.objects.filter(song_tag='2')
    tag_3 = Song.objects.filter(song_tag='3')
    tag_4 = Song.objects.filter(song_tag='4')
    tag_5 = Song.objects.filter(song_tag='5')
    tag_6 = Song.objects.filter(song_tag='6')

    return render(request, 'plist/tag.html',
                  {'tag_0': tag_0,
                   'tag_1': tag_1,
                   'tag_2': tag_2,
                   'tag_3': tag_3,
                   'tag_4': tag_4,
                   'tag_5': tag_5,
                   'tag_6': tag_6,
                   })
