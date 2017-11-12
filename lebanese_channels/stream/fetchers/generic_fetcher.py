from lebanese_channels import utils
from lebanese_channels.stream.stream_fetcher import StreamFetcher


class GenericStreamFetcher(StreamFetcher):
    def __init__(self, route_name, url):
        self.route_name = route_name
        self.url = url

    def get_route_name(self) -> str:
        return self.route_name

    def fetch_stream_url(self) -> str:
        html = utils.get_response(self.url)

        for line in html.splitlines():
            if 'file' in line and 'm3u8' in line:
                return line.split('"')[1]

        return ''