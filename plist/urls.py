from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('title/', views.search_title, name='title'),
    path('artist/', views.search_artist, name='artist'),
    path('album/', views.album, name='album'),
    path('genre/', views.search_genre, name='genre'),
    path('tag/', views.search_tag, name='tag'),
    path('event/', views.event, name='event'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('element/', views.element, name='element'),
    path('song/new/', views.song_new, name='song_new'),
    path('song/<int:pk>/', views.song_detail, name='song_detail'),
    path('mypage/playlist/', views.playlist, name='playlist'),
    path('mypage/playlist/<int:pk>/', views.play_detail, name='play_detail'),
]