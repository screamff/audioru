# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class AudioruItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field() # 歌名
    file_name = scrapy.Field() # .ts文件名
    file_content = scrapy.Field() # .ts文件内容


class MusicItem(scrapy.Item):
    """歌曲信息
    """
    m3u8_url = scrapy.Field() # m3u8文件地址
    title = scrapy.Field() # 歌名
    author = scrapy.Field() # 歌手
