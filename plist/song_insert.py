import pymysql
import os
import json

# read JSON file which is in the next parent folder
file = os.path.abspath('../music.json')
json_data = open(file).read()
json_obj = json.loads(json_data)


# do validation and checks before insert
def validate_string(val):
    if val != None:
        if type(val) is int:
            # for x in val:
            #   print(x)
            return str(val).encode('utf-8')
        else:
            return val


# connect to MySQL
con = pymysql.connect(host='192.168.35.169', user='project',
                      passwd='project', db='project_db')
cursor = con.cursor()
print(con, cursor)

# parse json data to SQL insert
for i, item in enumerate(json_obj):
    song_title = validate_string(item.get("song_title", None))
    song_artist = validate_string(item.get("song_artist", None))
    song_url = validate_string(item.get("song_url", None))
    song_genre = str(item.get("song_genre", None))
    song_tag = str(item.get("song_tag", None))
    song_detail = validate_string(item.get("song_detail", None))

    cursor.execute("INSERT INTO plist_song (song_title,song_artist,song_url,song_genre,song_tag,song_detail) VALUES (%s,%s,%s,%s,%s,%s)",
                   (song_title, song_artist, song_url, song_genre, song_tag, song_detail))

con.commit()
con.close()
