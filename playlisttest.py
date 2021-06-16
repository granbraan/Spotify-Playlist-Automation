import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = 'playlist-modify-public'
username = '22ng3bwo4cbdnf5b7nocchtfi'

token = SpotifyOAuth(scope=scope, username=username)
spotify_object = spotipy.Spotify(auth_manager=token)

#make playlsit
playlist_name = input("enter playlist name: ")
playlist_desc = input("enter playlist descript: ")

spotify_object.user_playlist_create(user=username,
 name=playlist_name, 
 public=True,
 description=playlist_desc)
