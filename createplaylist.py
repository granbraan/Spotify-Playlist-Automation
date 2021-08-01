import os

import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth
import random
import time

scope = 'playlist-modify-public user-read-recently-played playlist-read-private playlist-modify-private'
username = input("Enter your username: ")   


token = SpotifyOAuth(scope=scope, username=username)
spotify_object = spotipy.Spotify(auth_manager=token)
print("Pick an option\n")
print("1. Do you want to create a new playlist based on recently played songs\n")
print("2. Add new songs to a pre-existing playlist\n")
modify_options = input('Enter 1 or 2: ')

if(modify_options not in ['1','2']):
    modify_options = input('Enter 1 or 2: ')

if modify_options == '2':
    n = 4
    i = 0
    user_playlists = spotify_object.user_playlists(username,limit=4)
    json = json.dumps(user_playlists,indent=4,sort_keys=True)

    list_playlist_id = []
    list_playlist_names = []

    while i < n:
        user_uri = user_playlists["items"][i]["owner"]["uri"] #only user-created playlists are shown
        if(username in user_uri):
            playlist_name = user_playlists["items"][i]["name"]
            playlist_id = user_playlists["items"][i]["id"]
            print(f"{i+1}. {playlist_name}")
            list_playlist_id.append(playlist_id)
            list_playlist_names.append(playlist_name)
        i = i + 1 
    #pick playlist to add songs to
    
    playlist_choice = input('Which playlist would you like to add songs to? (input a number): ')
    while(int(playlist_choice) not in list(range(1,len(list_playlist_id)+1))):
        playlist_choice = input('Which playlist would you like to add songs to? (input a number): ')

    chosen_playlist = list_playlist_names[int(playlist_choice)-1]
    chosen_playlist_id = list_playlist_id[int(playlist_choice)-1]
    #get tracks and add into a list
    n = 100
    playlist_tracks = spotify_object.user_playlist_tracks(user=username,playlist_id=chosen_playlist_id,limit=n)
    track_name_list = []
    track_id_list = []
    track_artist_list = []
    i = 0
    
    try:
         while i < n:
            track_name = playlist_tracks['items'][i]['track']['name']
            track_id = playlist_tracks['items'][i]['track']['id']
            track_artist = playlist_tracks['items'][i]['track']['album']['artists'][0]['name']

            track_name_list.append(track_name)
            track_id_list.append(track_id)
            track_artist_list.append(track_artist)
            i = i + 1
    except IndexError:
        pass
    finally:
        pass

    #pick random tracks from playlist to get recommendations
    track_ids = []
    i=0
    while(i<5):
        randomized_track = random.randint(0,len(track_id_list)-1)
        track_ids.append(track_id_list[randomized_track])
        i = i+1

    #get recommended songs based on tracks
    num_recommended_songs = input("How many songs recommendations do you want?(min:1 max:100) ")
    while(int(num_recommended_songs) not in list(range(1,101))):
        num_recommended_songs = input("How many songs recommendations do you want?(min:1 max:100) ")
    recommended_songs = spotify_object.recommendations(seed_tracks=track_ids, limit=int(num_recommended_songs))

    print("Adding these tracks...")
    time.sleep(1)
    list_of_tracks = []
    for i in range(int(num_recommended_songs)):
        rs_track = recommended_songs['tracks'][i]['name']
        rs_artist = recommended_songs['tracks'][i]['album']['artists'][0]['name']
        rs_uri = recommended_songs['tracks'][i]['uri']
        list_of_tracks.append(rs_uri)

        print(f"{i+1}." + rs_artist + " - " + rs_track)
        time.sleep(0.1)

    spotify_object.user_playlist_add_tracks(user=username,playlist_id=chosen_playlist_id,tracks=list_of_tracks)
    

else:
    #make playlist
    playlist_name = input("enter playlist name: ")
    playlist_desc = input("enter playlist description: ")

    spotify_object.user_playlist_create(user=username,
    name=playlist_name, 
    public=True,
    description=playlist_desc)

    list_of_tracks = []

    #access and display recently played songs by user
    i = 0
    n = 20

    recent_track_ids = []

    recently_played_songs = spotify_object.current_user_recently_played(limit=n)
    print(f"Last {n} Recently Played Songs are\n")
    while (i<n):
        track_name = recently_played_songs['items'][i]['track']['name']
        track_id = recently_played_songs['items'][i]['track']['id']
        track_artist = recently_played_songs['items'][i]['track']['album']['artists'][0]['name']

        print(f"{i+1}. " + track_name + " by " + track_artist)
        i = i + 1

        recent_track_ids.append(track_id)
    #add 5 random tracks from recommended songs
    track_ids = []
    i=0
    while(i<5):
        randomized_track = random.randint(0,len(recent_track_ids)-1)
        track_ids.append(recent_track_ids[randomized_track])
        i = i+1

    #get recommended songs based on tracks
    num_recommended_songs = input("How many songs recommendations do you want?(min:1 max:100) ")
    while(int(num_recommended_songs) not in list(range(1,101))):
        num_recommended_songs = input("How many songs recommendations do you want?(min:1 max:100) ")
    recommended_songs = spotify_object.recommendations(seed_tracks=track_ids, limit=int(num_recommended_songs))

    print("Adding these tracks...")
    time.sleep(1)
    for i in range(int(num_recommended_songs)):
        rs_track = recommended_songs['tracks'][i]['name']
        rs_artist = recommended_songs['tracks'][i]['album']['artists'][0]['name']
        rs_uri = recommended_songs['tracks'][i]['uri']
        list_of_tracks.append(rs_uri)

        print(f"{i+1}." + rs_artist + " - " + rs_track)
        time.sleep(0.1)

    #find new generatedplaylist
    prePlaylist = spotify_object.user_playlists(user=username)
    playlist = prePlaylist['items'][0]['id']

    #add list of songs to the playlist
    spotify_object.user_playlist_add_tracks(user=username,playlist_id=playlist,tracks=list_of_tracks)