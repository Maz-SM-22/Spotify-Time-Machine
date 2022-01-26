import os 
import pprint
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyOAuth

date = input('Which year would you like to travel to? Enter the year in the following format YYYY-MM-DD: ')

URL = 'https://www.billboard.com/charts/hot-100/'
CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
ACCOUNT_ID = os.environ['SPOTIFY_ACCOUNT_ID']

if date: 
    response = requests.get(f'{URL}/{date}/')
else: 
    response = requests.get(URL)

page = response.content

soup = BeautifulSoup(page, 'html.parser')

rows = soup.find_all('div', class_="o-chart-results-list-row-container")
songs = [{'title': item.select_one('li h3').text.strip('\n'), 'artist': item.select('span[class*="a-no-trucate"]')[0].text.strip('\n')} for item in rows]

scope = 'playlist-modify-private'
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope, 
        client_id=CLIENT_ID, 
        client_secret=CLIENT_SECRET, 
        redirect_uri='https://example.com'
    )
)

tracks = []

for song in songs: 
    try: 
        track_data = sp.search(q=f"track: {song['title']} artist: {song['artist']}", limit=1)
        tracks.append(track_data)
    except: 
        continue

uris = []

for track in tracks: 
    try: 
        uri = track['tracks']['items'][0]['uri']
        uris.append(uri)
    except: 
        continue

playlist = sp.user_playlist_create(user=ACCOUNT_ID, name=f'{date} Billboard Top 100 (Almost)', public=False)
sp.playlist_add_items(playlist_id=playlist['id'], items=uris)