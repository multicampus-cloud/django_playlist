import os
import youtube_dl

VIDEO_DOWNLOAD_PATH = 'plist/static/plist/audio'  # 다운로드 경로


def download_video_and_subtitle(video_url, file_name):
    download_path = os.path.join(VIDEO_DOWNLOAD_PATH, file_name+'.%(ext)s')

    # for video_url in youtube_video:

    # youtube_dl options
    ydl_opts = {
        'format': 'bestaudio/best',  # 가장 좋은 화질로 선택(화질을 선택하여 다운로드 가능)
        'outtmpl': download_path, # 다운로드 경로 설정
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        print('video_url',video_url)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
    except Exception as e:
        print('error', e)


if __name__ == '__main__':

    youtube_url_list = [  # 유투브에서 다운로드 하려는 영상의 주소 리스트(아래는 Sample Video 리스트)
        "https://www.youtube.com/watch?v=baWt9Qre2fE",
    ]
    download_video_and_subtitle(youtube_url_list,'when')
    print('Complete download!')