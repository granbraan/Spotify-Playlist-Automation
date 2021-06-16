import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from spotifyclient import SpotifyClient

def main():

    spotify_client = SpotifyClient(os.getenv("SPOTIFY_AUTHORIZATION_TOKEN"), 
                                   os.getenv("SPOTIFY_USER_ID"))
    
    #get last played tracks
    num_last_played_tracks = int(input("How many previous songs do you want to base the new playlist off of: "))
    last_played_tracks = spotify_client.get_last_played_tracks(num_last_played_tracks)

    print(f"\nPrevious {num_last_played_tracks} songs listened on Spotify: ")
    for i, song in enumerate(last_played_tracks):
        print(f"{i+1} - {song}")
    
    # choose which tracks to use as a seed to generate a playlist
    indexes = input("\nEnter a list of up to 5 tracks you'd like to use as seeds. Use indexes separated by a space: ")
    indexes = indexes.split()
    seed_tracks = [last_played_tracks[int(index)-1] for index in indexes]

    # get recommended tracks based off seed tracks
    recommended_tracks = spotify_client.get_track_recommendations(seed_tracks)
    print("\nHere are the recommended tracks which will be included in your new playlist: ")
    for index, track in enumerate(recommended_tracks):
        print(f"{index+1}- {track}")

    # get playlist name from user and create playlist
    playlist_name = input("\nWhat's the playlist name? ")
    playlist_description = input("\nWhat's the playlist description?(Optional) ")
    playlist_public = input("\nShould the playlsit be public or private? ")
    playlist = spotify_client.create_playlist(playlist_name,playlist_description,playlist_public)
    print(f"\nPlaylist '{playlist.name}' was created successfully.")

    # populate playlist with recommended tracks
    spotify_client.populate_playlist(playlist, recommended_tracks)
    print(f"\nRecommended tracks successfully uploaded to playlist '{playlist.name}'.")


if __name__ == "__main__":
    main()