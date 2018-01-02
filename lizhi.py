from bs4 import BeautifulSoup
import requests
import os, sys
import json

# URL = "https://www.lizhi.fm/819298/14652243349936518"

fake_header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


def get_audio_url_from_json(audio_id):
    json_url  = "https://www.lizhi.fm/media/url/" + audio_id
    json_text = requests.get(json_url, headers=fake_header).text
    json_text = json.loads(json_text)
    return json_text['data']['url']


def get_audio_url(url):
    html = requests.get(URL, headers=fake_header).text
    soup = BeautifulSoup(html)
    div = soup.find('div', {'class': 'audio-controller'})
    audio_name = div['data-title']
    audio_id   = div['data-id']
    
    audio_url  = get_audio_url_from_json(audio_id)
    audio_url  = audio_url.split("lizhi.fm/")[-1]
    audio_url  = "http://www.lizhi.fm/" + audio_url
    audio_url  = audio_url.replace("_hd.mp3", "_sd.mp3")
    audio_url  = audio_url.replace("_ud.mp3", "_sd.mp3")
    file_type  = audio_url[-4:]
    return audio_url, audio_name + file_type

if __name__ == "__main__":
    URL = sys.argv[1]
    target = './static/downloads/'
    
    url, name = get_audio_url(URL)
    cmd = 'wget \"' + url + '\" -O \"' + target + name + '\" --header=\"User-Agent: ' + fake_header['User-Agent'] + '\"'
    os.system(cmd)
    print(cmd)

