import base64
import json
import os.path
import requests
import sys
import time

SPOTIFY_CLIENT_ID = ''
SPOTIFY_CLIENT_SECRET = ''

def get_access_token(code):
    # https://accounts.spotify.com/authorize?client_id=&response_type=code&redirect_uri=http%3A%2F%2Flocalhost&scope=user-library-read%20playlist-read-private
    client = SPOTIFY_CLIENT_ID + ':' + SPOTIFY_CLIENT_SECRET
    auth_token = base64.b64encode(client.encode()).decode()
    headers = {
            'Authorization': 'Basic ' + auth_token,
            'Content-Type': 'application/x-www-form-urlencoded'
            }
    payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': 'http://localhost'
            }
    result = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=payload).json()
    return result['access_token'], result['refresh_token']


def get_liked_songs(access_token, offset=0, limit=50):
    headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
            }
    result = requests.get('https://api.spotify.com/v1/me/tracks?offset={}&limit={}'.format(offset, limit), headers=headers).json()
    next_url = result['next']
    has_next = next_url is not None and len(next_url) > 0
    return result['items'], has_next


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please input code from url https://accounts.spotify.com/authorize?client_id=&response_type=code&redirect_uri=http%3A%2F%2Flocalhost&scope=user-library-read%20playlist-read-private')
        exit()
    code = sys.argv[1]
    access_token, _ = get_access_token(code)

    # load the previous list
    filepath = './spotify_liked_songs.json'
    items = []
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            items = json.load(f)

    # fetch liked songs
    has_next = True
    while has_next:
        try:
            new_items, new_has_next = get_liked_songs(access_token, offset=len(items))
            tracks = map(lambda i: i['track'], new_items)
            mapped = list(map(lambda i: { 'name': i['name'], 'artist_name': i['artists'][0]['name'], 'album_name': i['album']['name'] }, tracks))
            print('fetch success: {}'.format(list(map(lambda i: i['name'], mapped))))
            has_next = new_has_next
            # save the list
            with open(filepath, 'w') as f:
                json.dump(items, f, indent='\t')
                items.extend(mapped)
        except Exception as e:
            print('error happend: {}'.format(e))
        time.sleep(0.5)

