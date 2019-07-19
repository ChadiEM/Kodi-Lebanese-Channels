import logging

import flask
import flask_caching
from flask import Response

from lebanese_channels.channel_ids import CHANNEL_LIST
from lebanese_channels.display_item import DisplayItem

app = flask.Flask(__name__)
cache = flask_caching.Cache(app, config={'CACHE_TYPE': 'simple'})
wsgi_app = app.wsgi_app

logger = logging.getLogger(__name__)


@cache.cached(timeout=60)
def channel_stream():
    url_rule = flask.request.url_rule.rule
    target = url_rule.split('/channel/')[1]

    for channel in CHANNEL_LIST:
        if channel.get_route_name() == target:
            url = channel.get_stream_url()
            return flask.redirect(url, code=302)


for current_channel in CHANNEL_LIST:
    app.add_url_rule('/channel/' + current_channel.get_route_name(), view_func=channel_stream)


@app.route('/channels')
def channels_route_default():
    return __get_channels_response_lines(flask.request.url_root, flask.request.args.get('format'))


def __get_channels_response_lines(host: str, result_format: str) -> Response:
    display_items = []

    for channel in CHANNEL_LIST:
        url = host + 'channel/' + channel.get_route_name()
        display_items.append(
            DisplayItem(channel.get_route_name(), channel.get_name(), url, channel.get_logo()))

    if result_format is None or result_format == 'm3u8':
        response_list = ['#EXTM3U']
        for display_item in display_items:
            response_list.append('#EXTINF:-1'
                                 + ' tvg-id="' + display_item.channel_short_name + '"'
                                 + ' tvg-logo="' + display_item.channel_logo + '"'
                                 + ', ' + display_item.channel_name
                                 + '\n'
                                 + display_item.channel_url)

        return Response('\n'.join(response_list), mimetype='application/vnd.apple.mpegurl')
    elif result_format == 'html':
        response_list = []

        response_list.append('<!DOCTYPE html>')
        response_list.append('<html>')

        response_list.append('<head>')
        response_list.append('<title>Channel List</title>')
        response_list.append('</head>')

        response_list.append('<body>')
        response_list.append('<ul>')

        for display_item in display_items:
            response_list.append(
                '<li><a href="' + display_item.channel_url + '">' + display_item.channel_name + '</a></li>')

        response_list.append('</ul>')
        response_list.append('</body>')
        response_list.append('</html>')
        return Response('\n'.join(response_list), mimetype='text/html')
    else:
        return Response('Unknown Format', mimetype='text/plain')
