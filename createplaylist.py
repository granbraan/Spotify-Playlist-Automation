import os

import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth

scope = 'playlist-modify-public user-read-recently-played'
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

list_of_tracks = []

#access and display recently played songs by user
i = 0
n = 3

track_ids = []

recently_played_songs = spotify_object.current_user_recently_played(limit=n)
print(f"Last {n} Recently Played Songs are\n")
while (i<n):
    track_name = recently_played_songs['items'][i]['track']['name']
    track_id = recently_played_songs['items'][0]['track']['id']
    track_artist = recently_played_songs['items'][i]['track']['album']['artists'][0]['name']

    print(f"{i+1}. " + track_name + " by " + track_artist)
    i = i + 1

    track_ids.append(track_id)

#get recommended songs based on tracks
num_recommended_songs = input("How many songs recommendations do you want?(min:1 max:100) ")
recommended_songs = spotify_object.recommendations(seed_tracks=track_ids, limit=int(num_recommended_songs))

for i in range(int(num_recommended_songs)):
    rs_track = recommended_songs['tracks'][i]['name']
    rs_artist = recommended_songs['tracks'][i]['album']['artists'][0]['name']
    rs_uri = recommended_songs['tracks'][i]['uri']
    list_of_tracks.append(rs_uri)

    print(f"{i+1}." + rs_artist + " - " + rs_track)

#find new generatedplaylist
prePlaylist = spotify_object.user_playlists(user=username)
playlist = prePlaylist['items'][0]['id']

#add list of songs to the playlist
spotify_object.user_playlist_add_tracks(user=username,playlist_id=playlist,tracks=list_of_tracks)