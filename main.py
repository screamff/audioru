from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from audioru.spiders.audio_spider import DownloadMusicSpider

process = CrawlerProcess(get_project_settings())
process.crawl(DownloadMusicSpider)

process.start()
