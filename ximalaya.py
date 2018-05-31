
import requests
import json
import sys, os

fake_header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


def get_json_url(url):
  if url[-1] == '/':
    url = url[:-1]
  audio_id = url.split("/")[-1]
  json_url = "http://m.ximalaya.com/tracks/" + audio_id + ".json"
  return json_url


def get_json_audio_url(json_url):
  json_text = requests.get(json_url, headers=fake_header).text
  json_obj  = json.loads(json_text)
  audio_name = json_obj['title'] + '.m4a'

  if 'play_path_32' in json_obj:
    return json_obj['play_path_32'], audio_name
  elif 'play_path_64' in json_obj:
    return json_obj['play_path_64'], audio_name
  elif 'play_path' in json_obj:
    return json_obj['play_path'], audio_name
  else:
    return None, audio_name


if __name__ == "__main__":
  URL = sys.argv[1]
  target = './static/downloads/'
  
  json_url = get_json_url(URL)
  url, name = get_json_audio_url(json_url)
  cmd = 'wget \"' + url + '\" -O \"' + target + name + '\" --header=\"User-Agent: ' + fake_header['User-Agent'] + '\"'
  os.system(cmd)
  print(cmd)
