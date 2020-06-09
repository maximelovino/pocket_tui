
from config import Config
from cache import Cache
import googleapiclient.discovery
import googleapiclient.errors


class Youtube():
    def __init__(self, config: Config, cache: Cache):
        self.key = config.youtube_key
        api_service_name = "youtube"
        api_version = "v3"
        self.client = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=self.key)
        self.cache = cache

    def retrieve_video_channel(self, video_id: str) -> str:
        cache_channel = self.cache.retrieve_video_channel(video_id)

        if cache_channel is not None:
            return cache_channel
        
        request = self.client.videos().list(
            part="snippet",
            id=video_id
        )
        response = request.execute()
        try:
            vid = response["items"][0]
            channel_name = vid["snippet"]["channelTitle"]
        except:
            channel_name = "UNKNOWN CHANNEL"
        self.cache.save_video_channel(video_id, channel_name)
        return channel_name
