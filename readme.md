### 从audioru下载歌曲
通过歌名，歌手下载歌曲

#### 使用
1. 配置代理`middlewars.py` 设置 `request.meta["proxy"]`为你的代理服务器
2. `middlewares.py`设置`ffmpeg.exe`路径, 自行下载ffmpeg, 本代码不提供
```
current_folder = Path(__file__).resolve().parent
out_path = current_folder / 'temp' # 歌曲下载目录
exe_path = out_path / 'ffmpeg.exe' # ffmpeg路径
```
3. `audio_spider.py`中配置搜索关键词

```
class DownloadMusicSpider(scrapy.Spider):
    name = 'downloadmusic'
    keyword = '夜曲'  # 歌名
    author = '周杰伦' # 歌手
    ...
```
4. 运行main.py