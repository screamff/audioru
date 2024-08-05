# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pathlib import Path
import subprocess
import json
from scrapy.exceptions import DropItem

current_folder = Path(__file__).resolve().parent
out_path = current_folder / 'temp' # 歌曲下载目录
exe_path = out_path / 'ffmpeg.exe' # ffmpeg路径
out_path.mkdir(parents=True, exist_ok=True)

class AudioruPipeline:

    def __init__(self):
        self.items = []

    def process_item(self, item, spider):
        if item.get('file_name'):
            self.items.append(item)
        return item

    def close_spider(self, spider):
        if self.items:
            sorted_items = sorted(self.items, key=lambda x: x["file_name"])
            name = self.items[0].get('name').strip() + '.ts'
            file_path = out_path / name
            with open(file_path, 'wb') as f:
                for item in sorted_items:
                    f.write(item['file_content'])
            name = self.items[0].get('name').strip() + '.mp3'
            output_file = out_path / name
            command = f"{exe_path} -i {file_path} -vn -ar 44100 -ac 2 -b:a 320k -y {out_path / output_file}"
            subprocess.call(command, shell=False)


class MusicPipeline:
    def open_spider(self, spider):
        self.items = []

    def close_spider(self, spider):
        with open(out_path / "results.json", "w", encoding='utf-8') as file:
            json.dump(self.items, file, ensure_ascii=False, indent=2)

    def process_item(self, item, spider):
        if item.get('m3u8_url'):
            self.items.append(dict(item))
        return item
