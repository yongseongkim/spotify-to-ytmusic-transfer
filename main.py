import base64
import json
import requests

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from ytmusicapi import YTMusic

def auth_yt():
    flow = InstalledAppFlow.from_client_secrets_file('./client_secret.json', scopes=['https://www.googleapis.com/auth/youtube'])
    credentials = flow.run_console()
    return biuild('youtube', 'v3', credentials=credentials)


def like_ytmusic(yt, song_id):
    yt.videos().rate(id=song_id, rating='like').execute()


def search_yt_music(ytmusic, keyword):
    results = ytmusic.search(keyword)
    # filter results or mapping


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
# ytmusic = YTMusic(ytmusic_auth)
# yt = auth_youtube()

SPOTIFY_CLIENT_ID = ''
SPOTIFY_CLIENT_SECRET = ''

def auth_sptf(): 
    client = SPOTIFY_CLIENT_ID + ':' + SPOTIFY_CLIENT_SECRET
    auth_token = base64.b64encode(client.encode()).decode()
    print(auth_token)
    headers = {
            'Authorization': 'Basic ' + auth_token,
            'Content-Type': 'application/x-www-form-urlencoded'
            }
    payload = {
            'grant_type': 'client_credentials'
            }
    result = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=payload)
    return result.json()['aceess_token']

access_token = auth_sptf()

