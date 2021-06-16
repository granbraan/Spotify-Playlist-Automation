import os
from track import Track
import spotipy
import json
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
#search song
song_input = input("Enter song name: ")
los = []

while song_input != 'finish':
    result = spotify_object.search(q=song_input)

    track_name = result['tracks']['items'][0]['name']
    track_artist = result['tracks']['items'][0]['album']['artists'][0]['name']

    los.append(result['tracks']['items'][0]['uri'])
    print(track_name + " by " + track_artist)

    song_input = input("Enter another song: ")

#find new generatedplaylist
prePlaylist = spotify_object.user_playlists(user=username)
playlist = prePlaylist['items'][0]['id']

#add list of songs to the playlist
spotify_object.user_playlist_add_tracks(user=username,playlist_id=playlist,tracks=los)






