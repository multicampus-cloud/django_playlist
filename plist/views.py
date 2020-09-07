from .forms import SongForm,UserForm, LoginForm, PlaylistForm
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


@login_required
def list_new(request):
    song_list = Song.objects.all()
    if request.method == "POST":
        form = PlaylistForm(request.POST)
        if form.is_valid():
            
            # db에 넣기
            playlist = Playlist.objects.create(play_title=form.cleaned_data['play_title'],
                                                author=request.user,
                                                play_list='empty',
                                                play_detail='노래리스트가 없습니다.',
                                        )
            return redirect('playlist')
        else:
            return HttpResponse('문제가 발생했습니다. 다시 시도해주세요.')
    
    else:
        form = PlaylistForm()
        return render(request, 'plist/list_new.html', {'form':form, 'song_list':song_list})


# 다른 사람 플레이 리스트 -> 내 플레이리스트에 추가
@login_required
def list_copy(request,pk):
    # 다른 사람 플레이리스트 가져오기
    playlist = get_object_or_404(Playlist,pk=pk)
    # 로그인 사용자 계정으로 플레이리스트 db에 추가
    playlist = Playlist.objects.create(play_title=playlist.play_title,
                            author=request.user,
                            play_list=playlist.play_list,
                            play_detail=str(playlist.author)+'의 플레이리스트 copy',
                            )

    return redirect('playlist')


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


# new song 만들기
@login_required
def song_new(request):
    if request.method == "POST":
        form = SongForm(request.POST)
        if form.is_valid():
            # 파일뽑아내는 작업
            download_video_and_subtitle(form.cleaned_data['song_url'], form.cleaned_data['song_title'])

            # 파일 자르는 작업
            song_slice(form.cleaned_data['song_title'],form.cleaned_data['song_start'],form.cleaned_data['song_end'])

            # 썸네일 만드는 작업
            verify = get_thumbnail(form.cleaned_data['song_artist'])
            if verify:
                thumbnail = form.cleaned_data['song_artist']
            else:
                thumbnail = 'default'

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
        return render(request, 'plist/song_new.html', {'form': form})


# 특정 song detail 정보 가져오기
def song_detail(request,pk):
    song = get_object_or_404(Song, pk=pk)
    song_tag = TAG_CHOICES[int(song.song_tag)]
    song_genre = GENRE_CHOICES[int(song.song_genre)]
    # 추천 노래 리스트 받아오기
    recommend_list = recommend_song_list(song.song_url)
    return render(request, 'plist/song_detail.html', \
                  {'song': song,'genre':song_genre[1], 'tag':song_tag[1],\
                   'recommend_list':recommend_list})


# 메인 페이지
def index(request):
    my_song_list = Song.objects.all()

    # 전체 플레이 리스트 데이터를 가져옴
    event_all_list = Playlist.objects.all()
    eventlist = []
    # 전체 플레이 리스트 데이터만큼 디테일을 만듬
    for detail_list in event_all_list:
        list_dict = {}
        song_list = []
        # 디테일 리스트에 노래가 비어있으면 무시
        if detail_list.play_list == 'empty':
            continue
        # 디테일 리스트에 노래들이 있으면 노래들을 리스트로 패킹(아직은 키값으로 유지)
        else:
            song_id_list = detail_list.play_list.split(',')
            # 리스트화된 노래들을 하나씩 뿌려줌(song에 있는 키값과 매칭)
            for song_id in song_id_list:
                song = get_object_or_404(Song, pk=song_id)
                # song에 있는 노래들을 하나씪 뿌려줘서 개별적으로 나타냄
                song_list.append(song)
            list_dict['my_playlist'] = detail_list
            list_dict['song_list'] = song_list
            eventlist.append(list_dict)
            eventlist = eventlist[-3:]
    return render(request, 'plist/index.html', {'eventlist': eventlist, 'my_song_list':my_song_list})


def event(request):
    # 전체 플레이 리스트 데이터를 가져옴
    event_all_list = Playlist.objects.all()
    eventlist = []
    # 전체 플레이 리스트 데이터만큼 디테일을 만듬
    for detail_list in event_all_list:
        list_dict = {}
        song_list = []
        # 디테일 리스트에 노래가 비어있으면 무시
        if detail_list.play_list == 'empty':
            continue
        # 디테일 리스트에 노래들이 있으면 노래들을 리스트로 패킹(아직은 키값으로 유지)
        else:
            song_id_list = detail_list.play_list.split(',')
            # 리스트화된 노래들을 하나씩 뿌려줌(song에 있는 키값과 매칭)
            for song_id in song_id_list:
                song = get_object_or_404(Song, pk=song_id)
                # song에 있는 노래들을 하나씪 뿌려줘서 개별적으로 나타냄
                song_list.append(song)
            list_dict['my_playlist'] = detail_list
            list_dict['song_list'] = song_list
            eventlist.append(list_dict)

    return render(request, 'plist/event1.html', {'eventlist': eventlist})


# mypage 안에 my playlist 가져오기(모든 노래가져오기) + playlist 목록 가져오기
@login_required
def playlist(request):
    # 페이지 별로 구분해서 리스트 출력하기
    song_list = Song.objects.filter(author=request.user)
    # song_list 목록에서 한페이지당 2개씩 할당
    paginator = Paginator(song_list, 5)
    # page 받아오기
    page = request.GET.get('page')

    try:
        song_list = paginator.page(page)
    except PageNotAnInteger:
        song_list = paginator.page(1)
    except EmptyPage:
        song_list = paginator.page(paginator.num_pages)

    # 플레이리스트 가져오기
    play_list = Playlist.objects.filter(author=request.user)

    return render(request, 'plist/myPage/playlist.html', {'song_list': song_list, 'play_list': play_list})


# 특정 playlist 들어있는 노래목록 가져오기
def play_detail(request, pk):
    play_detail_list = get_object_or_404(Playlist, pk=pk)

    song_list = []
    # song 추가되어 있을 경우에만 song객체 가져오기
    if play_detail_list.play_list != 'empty':
        song_id_list = play_detail_list.play_list.split(',')
        for song_id in song_id_list:
            song = get_object_or_404(Song,pk=song_id)
            song_list.append(song)
        verify = True
    else:
        verify = False

    return render(request, 'plist/myPage/play_detail.html', {'play_detail_list': play_detail_list, 'song_list':song_list,'verify':verify})


@login_required
def search_title(request):
    q = request.GET.get('q')
    if q:
        songs = SongDocument.search().query('match',song_title=q)
    else:
        songs = ''

    # 플레이리스트 가져오기
    play_list = Playlist.objects.filter(author=request.user)

    return render(request, 'plist/title.html',{'songs':songs,'play_list':play_list})


@login_required
def search_artist(request):
    a = request.GET.get('a')
    if a:
        singer = SongDocument.search().query('match',song_artist=a)
    else:
        singer = ''

    # 플레이리스트 가져오기
    play_list = Playlist.objects.filter(author=request.user)

    return render(request, 'plist/artist.html', {'singer':singer,'play_list':play_list})


@login_required
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

    # 플레이리스트 가져오기
    play_list = Playlist.objects.filter(author=request.user)

    return render(request, 'plist/genre.html',
                  {'kpops': kpops,
                   'pops': pops,
                   'r_bs': r_bs,
                   'jazzs': jazzs,
                   'indies':indies,
                   'dances': dances,
                   'hiphops':hiphops,
                   'elses': elses,
                   'play_list': play_list,
                   })


@login_required
def search_tag(request):
    # return render(request,'plist/genre.html')
    tag_0 = Song.objects.filter(song_tag='0')
    tag_1 = Song.objects.filter(song_tag='1')
    tag_2 = Song.objects.filter(song_tag='2')
    tag_3 = Song.objects.filter(song_tag='3')
    tag_4 = Song.objects.filter(song_tag='4')
    tag_5 = Song.objects.filter(song_tag='5')
    tag_6 = Song.objects.filter(song_tag='6')

    # 플레이리스트 가져오기
    play_list = Playlist.objects.filter(author=request.user)

    return render(request, 'plist/tag.html',
                  {'tag_0': tag_0,
                   'tag_1': tag_1,
                   'tag_2': tag_2,
                   'tag_3': tag_3,
                   'tag_4': tag_4,
                   'tag_5': tag_5,
                   'tag_6': tag_6,
                   'play_list':play_list,
                   })


@login_required
def my_info(request):
    my_playlists = Playlist.objects.filter(author=request.user)
    info_list = []

    for detail_list in my_playlists:
        list_dict = {}
        song_list = []

        if detail_list.play_list == 'empty':
            verify = False
        else:
            verify = True
            song_id_list = detail_list.play_list.split(',')
            for song_id in song_id_list:
                song = get_object_or_404(Song, pk=song_id)
                song_list.append(song)

        list_dict['my_playlist'] = detail_list
        list_dict['song_list'] = song_list
        list_dict['verify'] = verify
        info_list.append(list_dict)

    # print(info_list)
    return render(request, 'plist/myPage/my_info.html', {'info_list': info_list})


@login_required
def delete_playlist(request,pk):
    del_playlist = get_object_or_404(Playlist, pk=pk)
    del_playlist.delete()
    return redirect('my_info')


@login_required
def delete_song(request, play_pk, song_pk):
    select_playlist = get_object_or_404(Playlist, pk=play_pk)
    del_pk = song_pk
    song_list = select_playlist.play_list.split(',')
    for i in song_list:
        if str(del_pk) == i:
            song_list.remove(str(del_pk))
    new_list = ",".join(song_list)
    select_playlist.play_list = new_list
    select_playlist.save()
    return redirect('my_info')


@login_required
def rename_playlist(request,pk):
    re_playlist = get_object_or_404(Playlist, pk=pk)
    if request.method == "POST":
        form = PlaylistForm(request.POST)
        if form.is_valid():
            re_playlist.play_title = form.cleaned_data['play_title']
            re_playlist.save()
            return redirect('my_info')
        else:
            return HttpResponse('문제가 발생했습니다. 다시 시도해주세요.')

    else:
        form = PlaylistForm(instance=re_playlist)
        return render(request, 'plist/myPage/rename_playlist.html', {'form': form})


@login_required
def add_song(request, play_pk, song_pk, path_pk):
    new_playlist = get_object_or_404(Playlist, pk=play_pk)

    if new_playlist.play_list != 'empty':
        song_list = new_playlist.play_list.split(',')
        play_detail = new_playlist.play_detail+'\n'
    else:
        song_list = []
        play_detail = ''

    if str(song_pk) not in song_list:
        song_list.append(str(song_pk))
        new_list = ",".join(song_list)
        new_playlist.play_list = new_list

        song = get_object_or_404(Song,pk=song_pk)
        play_detail += song.song_title
        new_playlist.play_detail = play_detail

        new_playlist.save()


    # 1: playlist 로 보내기
    if path_pk == 1:
        return redirect('playlist')
    # 2: artist 로 보내기
    elif path_pk == 2:
        return redirect('artist')
    # 3: title 로 보내기
    elif path_pk == 3:
        return redirect('title')
    # 4: genre 로 보내기
    elif path_pk == 4:
        return redirect('genre')
    # 5: tag 로 보내기
    elif path_pk == 5:
        return redirect('tag')

def myinfo_songlist(request):
    if request.user.id == 5:
        song_list = Song.objects.all()
    else:
        song_list = Song.objects.filter(author=request.user)
    return render(request,'plist/myPage/songlist.html',{'song_list':song_list})


def remove_song(request, pk):
    songs_list = Song.objects.filter(author=request.user)
    if request.user.id == 5:
        for song in songs_list:
            if song.id == pk:
                songs_list.remove(song)
                song.delete()
    # else:
    #     for song in songs_list:
    #         if song.id == pk:
    #             song.author = 'project'
    #             song.save()
    return redirect('songs')
