import json
import sys

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from ytmusicapi import YTMusic


def auth_yt():
    flow = InstalledAppFlow.from_client_secrets_file('./client_secret.json', scopes=['https://www.googleapis.com/auth/youtube'])
    credentials = flow.run_console()
    return build('youtube', 'v3', credentials=credentials)


def like_ytmusic(yt, song_id):
    yt.videos().rate(id=song_id, rating='like').execute()


def search_yt_music(ytmusic, keyword):
    try:
        results = ytmusic.search(keyword, 'songs')
        if len(results) == 0:
            return None
        top = results[0]
        return {
                'video_id': top['videoId'],
                'title': top['title'],
                'album_name': top['album']['name'],
                'artist_name': top['artists'][0]['name'],
                'duration_seconds': top['duration_seconds'],
                'url': 'https://music.youtube.com/watch?v={}'.format(top['videoId'])
                }
    except Exception as e:
        print('error happend {}'.format(e))
        return None


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please input playlist json path')
        exit()

    yt = auth_yt()

    # load the liked songs
    filepath = sys.argv[1]
    items = []
    with open(filepath, 'r') as f:
        items = json.load(f)

    # search by keyword
    ytmusic_auth = '''
    {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Aceept-Language": "ko,en-US;q=0.9,en;q=0.8",
        "Content-Type": "application/json",
        "X-Goog-AuthUser": "0",
        "x-origin": "https://music.youtube.com",
        "cookie": ""
    }
    '''
    ytmusic = YTMusic(ytmusic_auth)
    for item in items:
        result = search_yt_music(ytmusic, item['artist_name'] + ' ' + item['name'])
        if result is not None:
            print('{} is searched. {}'.format(result['title'] + ' ' + result['artist_name'], result['url']))
            like_ytmusic(yt, result['video_id'])

