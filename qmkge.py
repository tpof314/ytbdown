import requests
import re
import sys, os
from bs4 import BeautifulSoup

fake_header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

def getAudioTag(tags):
	for tag in tags:
		if 'playurl' in str(tag.text):
			return str(tag.text)
	return None

def get_audio_url(url):
	resp = requests.get(url, headers=fake_header)
	html = resp.text
	soup = BeautifulSoup(html, "html.parser")
	tags = soup.findAll('script', attrs={'type': 'text/javascript'})
	tag  = getAudioTag(tags)
	result_url   = re.search('http://[a-z][a-z].stream.kg.qq.com/.*\.m4a', tag)
	extension    = '.m4a'
	if result_url == None:
		result_url   = re.search('http://[a-z][a-z].stream.kg.qq.com/.*\.mp4', tag)
		extension    = '.mp4'
	result_url   = result_url.group(0)
	result_title = soup.find('title').text + extension
	return result_url, result_title

"""
URL = "https://node.kg.qq.com/play?s=QWFfTvQ2odtr4QXS&shareuid=649e958226283e8230&topsource=a0_pn201001003_z11_u638735994_l1_t1531481363__"
download(URL)
"""

if __name__ == "__main__":
  URL = sys.argv[1]
  target = './static/downloads/'
  
  url, name = get_audio_url(URL)
  cmd = 'wget \"' + url + '\" -O \"' + target + name + '\" --header=\"User-Agent: ' + fake_header['User-Agent'] + '\"'
  os.system(cmd)
  print(cmd)
