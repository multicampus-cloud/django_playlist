from pydub import AudioSegment

STATIC_SONG_PATH = 'plist/static/plist/audio/'


# 초 계산 함수
# 입력값 예시   9:10
def find_sec(input_time):
    input_time = str(input_time)
    print(input_time)
    min_sec = input_time.split(':')

    if len(min_sec) ==3 :
        hour = int(min_sec[0])
        min = int(min_sec[1])
        sec = int(min_sec[2])
    else :
        hour = 0
        min = int(min_sec[0])
        sec = int(min_sec[1])

    return int(hour)*60*60*1000 + int(min) * 60 * 1000 + int(sec) * 1000

# print(find_sec('9:10'))


# mp3 slice 함수
def song_slice(song_name,start,end):

    # 시작/종료 초 가져오기
    # Time to miliseconds
    startTime = find_sec(start)
    endTime = find_sec(end)
    print(startTime, endTime)

    try:
        # Opening file and extracting segment
        audio_file = STATIC_SONG_PATH+song_name+'.mp3'
        song = AudioSegment.from_mp3(audio_file)
        extract = song[startTime:endTime]

        # Saving
        extract.export(audio_file, format='mp3')
    except Exception as e:
        print('error:',e)


if __name__ == '__main__':
    song_slice('when','20:03','23:24')