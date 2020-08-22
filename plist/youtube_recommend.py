import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

url = 'https://www.youtube.com/watch?v=Bl4dfyDTXmU'

req_headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
}

response = requests.get(url,headers=req_headers)
print(response.status_code)


html = response.text
soup = BeautifulSoup(html,'html.parser')
#
# print(soup)


regex_filter = r'title":{"accessibility".*?"commandMetadata":{"webCommandMetadata":{"url":"/watch\?v=.*?"'

regex_list = re.findall(r'title":{"accessibility".*?"commandMetadata":{"webCommandMetadata":{"url":"/watch\?v=.*?"',str(soup))


# for regex in regex_list:
#     print(regex)
#     print("="*100)


for regex in regex_list[:3]:
    print(regex)
    regex = re.sub('title":{"accessibility":{"accessibilityData":{"label":"','',str(regex))
    title = re.split('게시자',str(regex))
    print(title[0])
    url = re.split('"commandMetadata":{"webCommandMetadata":{"url":"',str(regex))[-1]
    #print(url)
    link = urljoin('https://www.youtube.com', url)
    print(link)
    print("="*100)




