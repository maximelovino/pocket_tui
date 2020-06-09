from typing import Union
import os
from pathlib import Path
import diskcache as dc


CACHE_BASE_FOLDER = os.path.join(Path.home(), ".cache")
CACHE_POCKET_CLI = os.path.join(CACHE_BASE_FOLDER, "pocket_cli")
CACHE_YOUTUBE = os.path.join(CACHE_POCKET_CLI, "youtube")
CACHE_TOKEN_FILE = os.path.join(CACHE_POCKET_CLI, ".token")


class Cache():
    def __init__(self):
        if not os.path.isdir(CACHE_POCKET_CLI):
            print("Creating new cache directory")
            os.makedirs(CACHE_POCKET_CLI)
        self.youtube_cache = dc.Cache(CACHE_YOUTUBE)

    def get_cached_token(self) -> Union[str, None]:
        if os.path.exists(CACHE_TOKEN_FILE):
            with open(CACHE_TOKEN_FILE, 'r') as f:
                token = f.read()
                return token
        else:
            return None

    def save_cached_token(self, token: str) -> None:
        with open(CACHE_TOKEN_FILE, 'w') as f:
            f.write(token)

    def retrieve_video_channel(self, video_id: str) -> Union[str, None]:
        if video_id in self.youtube_cache:
            return self.youtube_cache[video_id]
        else:
            return None

    def save_video_channel(self, video_id: str, channel: str) -> None:
        self.youtube_cache[video_id] = channel
