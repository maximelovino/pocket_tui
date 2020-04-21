from datetime import datetime
from urllib.parse import urlparse, parse_qs
import tldextract
from typing import List


YOUTUBE_LONG_DOMAIN = "youtube.com"
YOUTUBE_SHORT_DOMAIN = "youtu.be"

class Entry():
    def __init__(self, entry_dict):
        super().__init__()
        self.id = entry_dict['item_id']
        self.title = entry_dict['resolved_title']
        self.url = entry_dict['resolved_url']
        self.updated = datetime.utcfromtimestamp(int(entry_dict['time_updated']))
        self.added = datetime.utcfromtimestamp(int(entry_dict['time_added']))
        extracted = tldextract.extract(self.url)
        self.domain = extracted.registered_domain

    @staticmethod
    def parse(entry_dict) -> '__class__':
        url = entry_dict['resolved_url']
        extracted = tldextract.extract(url)
        domain = extracted.registered_domain
        if domain == YOUTUBE_LONG_DOMAIN or domain == YOUTUBE_SHORT_DOMAIN:
            return VideoEntry(entry_dict)
        else:
            return ArticleEntry(entry_dict)

    @staticmethod
    def parse_list(xs) -> List['__class__']:
        return list(map(lambda x: Entry.parse(x), xs))

    def __str__(self):
        return f"{self.id}\n{self.title}\n{self.url}\nAdded:{self.added} - Updated: {self.updated}\nDomain: {self.domain}"

class ArticleEntry(Entry):
    def __init__(self, entry_dict):
        super().__init__(entry_dict)

class VideoEntry(Entry):
    def __init__(self, entry_dict):
        super().__init__(entry_dict)
        self.video_id = self.retrieve_video_id()

    def retrieve_video_id(self) -> str:
        if self.domain == YOUTUBE_LONG_DOMAIN:
            return parse_qs(urlparse(self.url).query)['v'][0]
        elif self.domain == YOUTUBE_SHORT_DOMAIN:
            return urlparse(self.url).path[1:]

    def __str__(self):
        return f"YOUTUBE\n{super().__str__()}\nID: {self.video_id}"
