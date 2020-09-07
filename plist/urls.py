from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('myPage/myInfo/',views.my_info, name='my_info'),
    path('title/', views.search_title, name='title'),
    path('artist/', views.search_artist, name='artist'),
    path('genre/', views.search_genre, name='genre'),
    path('tag/', views.search_tag, name='tag'),
    path('event/', views.event, name='event'),
    path('song/new/', views.song_new, name='song_new'),
    path('song/<int:pk>/', views.song_detail, name='song_detail'),
    path('mypage/playlist/', views.playlist, name='playlist'),
    path('mypage/playlist/<int:pk>/', views.play_detail, name='play_detail'),
    path('mypage/playlist/new/', views.list_new, name='list_new'),
    path('mypage/playlist/copy/<int:pk>/', views.list_copy, name='list_copy'),
    path('myPage/myInfo/delete/<int:pk>', views.delete_playlist, name='delete_playlist'),
    path('myPage/myInfo/delete/<int:play_pk>/<int:song_pk>/', views.delete_song, name='delete_song'),
    path('myPage/myInfo/rename/<int:pk>/',views.rename_playlist,name='rename_playlist'),
    path('add/song/<int:play_pk>/<int:song_pk>/<int:path_pk>/', views.add_song, name='add_song'),
    path('myPage/myInfo/songs/', views.myinfo_songlist, name='songs'),
    path('myPage/myInfo/songs/<int:pk>/',views.remove_song,name='remove_song'),
]
