from lxml.html import parse
from lxml import html
import requests


def get_lyrics():
    page = requests.get('http://www.allthelyrics.com/lyrics/2pac')
    tree = html.fromstring(page.content)
    songs_links = tree.xpath('//ul/li/a/@href')
    print ('Links: ', len(songs_links))
    lyrics = []
    for x in range(0, 100):
        if songs_links[x].__contains__("lyrics/2pac"):
            try:
                url = "http://www.allthelyrics.com" + songs_links[x]
                song_page = parse(url)
                root = song_page.getroot()
                songs_words = root.xpath('//div[@class="content-text-inner"]/p/text()')
                lyrics.append(songs_words)
            except ValueError:
                continue
    return lyrics
