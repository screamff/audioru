from pathlib import Path
import re
import difflib
import scrapy
from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES
from audioru.items import MusicItem, AudioruItem
import m3u8


class DownloadMusicSpider(scrapy.Spider):
    name = 'downloadmusic'
    keyword = '夜曲'  # 歌名
    author = '周杰伦' # 歌手
    start_urls = [f'https://web.ligaudio.ru/mp3/{keyword}']

    def calculate_similarity(self, song, target_artist, target_song):
        artist_similarity = difflib.SequenceMatcher(None, song.get('author'), target_artist).ratio()
        song_similarity = difflib.SequenceMatcher(None, song.get('title'), target_song).ratio()
        return artist_similarity + song_similarity

    def parse(self, response):
        """解析搜索结果, 提取匹配度最高的结果"""
        results = []
        for music in response.css(".item .play"):
            m3u8_url = music.attrib.get('data-audio')
            m3u8_url = m3u8_url.replace('//', 'https://')
            title = music.xpath("..").css('.title::text').get()
            author = music.xpath("..").css('.autor a::text').get()
            item = MusicItem(m3u8_url=m3u8_url, title=title, author=author)
            results.append(item)

        best_match = max(results, key=lambda song: self.calculate_similarity(song, self.author, self.keyword))
        print(f'正在下载歌曲:\n{best_match}')
        yield scrapy.Request(best_match.get('m3u8_url'), self.parse_m3u8)

    def parse_m3u8(self, response):
        """解析目标m3u8信息, 准备下载"""
        playlist = m3u8.loads(response.text)
        for key in playlist.keys:
            segments = playlist.segments.by_key(key)
            if key.uri:
                yield scrapy.Request(key.uri, self.get_key, cb_kwargs={'segments': segments})
            else:
                for seg in segments:
                    yield scrapy.Request(seg.uri, self.download_uncrypeted_data)

    def download_uncrypeted_data(self, response):
        seg_no = re.findall(r'(.*?).ts', response.url.split('/')[-1])
        if seg_no:
            yield AudioruItem(name=self.keyword, file_name=f'{seg_no[0]}.ts', file_content=response.body)

    def download_crypeted_data(self, response, key):
        # 创建aes解密器
        cipher = AES.new(key, AES.MODE_CBC)
        # 解密数据
        decrypted_data = cipher.decrypt(response.body)
        seg_no = re.findall(r'(.*?).ts', response.url.split('/')[-1])
        if seg_no:
            yield AudioruItem(name=self.keyword, file_name=f'{seg_no[0]}.ts', file_content=decrypted_data)

    def get_key(self, response, segments):
        key = response.body
        for seg in segments:
            yield scrapy.Request(seg.uri, self.download_crypeted_data, cb_kwargs={'key': key})


class SearchMusciSpider(scrapy.Spider):
    """"搜索歌曲, 结果存储在temp/results.json"""
    name = 'searchmusic'
    keyword = '夜曲' # 歌名
    start_urls = [f'https://web.ligaudio.ru/mp3/{keyword}']

    def parse(self, response):
        for music in response.css(".item .play"):
            m3u8_url = music.attrib.get('data-audio')
            m3u8_url = m3u8_url.replace('//', 'https://')
            title = music.xpath("..").css('.title::text').get()
            author = music.xpath("..").css('.autor a::text').get()
            item = MusicItem(m3u8_url=m3u8_url, title=title, author=author)
            print(item)
            yield item