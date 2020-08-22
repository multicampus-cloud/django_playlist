with open('./static/plist/audio/test2.mp3','rb') as f:
    data = f.read()

bytes = len(data)
print(bytes)