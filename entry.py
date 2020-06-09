from datetime import datetime
import webbrowser
from urllib.parse import urlparse, parse_qs
import tldextract
from typing import List, Tuple
import diskcache as dc
from dotenv import load_dotenv
from youtube import Youtube
import os


YOUTUBE_LONG_DOMAIN = "youtube.com"
YOUTUBE_SHORT_DOMAIN = "youtu.be"


class Entry():
    def __init__(self, entry_dict):
        super().__init__()
        self.id = entry_dict['item_id']
        self.title = entry_dict['resolved_title']
        self.url = entry_dict['resolved_url']
        self.updated = datetime.utcfromtimestamp(
            int(entry_dict['time_updated']))
        self.added = datetime.utcfromtimestamp(int(entry_dict['time_added']))
        extracted = tldextract.extract(self.url)
        self.domain = extracted.registered_domain

    @staticmethod
    def parse(entry_dict, youtube: Youtube) -> '__class__':
        url = entry_dict['resolved_url']
        extracted = tldextract.extract(url)
        domain = extracted.registered_domain
        if domain == YOUTUBE_LONG_DOMAIN or domain == YOUTUBE_SHORT_DOMAIN:
            return VideoEntry(entry_dict, youtube)
        else:
            return ArticleEntry(entry_dict)

    @staticmethod
    def parse_list(xs, youtube: Youtube) -> List['__class__']:
        return list(map(lambda x: Entry.parse(x,youtube), xs))

    def list_str(self) -> str:
        pass

    def open(self):
        pass

    def domain_filter(self) -> str:
        pass

    def __str__(self):
        return f"{self.id}\n{self.title}\n{self.url}\nAdded:{self.added} - Updated: {self.updated}\nDomain: {self.domain}"


class ArticleEntry(Entry):
    def __init__(self, entry_dict):
        super().__init__(entry_dict)

    def list_str(self):
        return f"{self.domain} => {self.title}"

    def open(self):
        webbrowser.open(self.url, new=2, autoraise=False)

    def domain_filter(self):
        return self.domain


class VideoEntry(Entry):
    def __init__(self, entry_dict, youtube: Youtube):
        super().__init__(entry_dict)
        self.youtube = youtube
        self.video_id = self.extract_video_id()
        self.channel = self.retrieve_video_channel()

    def extract_video_id(self) -> str:
        if self.domain == YOUTUBE_LONG_DOMAIN:
            return parse_qs(urlparse(self.url).query)['v'][0]
        elif self.domain == YOUTUBE_SHORT_DOMAIN:
            return urlparse(self.url).path[1:]

    def retrieve_video_channel(self) -> str:
        return self.youtube.retrieve_video_channel(self.video_id)

    def list_str(self):
        return f"{self.channel} => {self.title}"

    def open(self):
        os.system(f"mpv {self.url}")

    def domain_filter(self):
        return self.channel

    def __str__(self):
        return f"YOUTUBE\n{super().__str__()}\nID: {self.video_id}"
