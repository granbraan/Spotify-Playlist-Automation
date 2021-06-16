import json
import requests
import spotipy


from track import Track
from playlist import Playlist

class SpotifyClient:
    #Performs varius tasks using Spotify Api

    def __init__(self, authorization_token, user_id):
        self.authorization_token = authorization_token
        self.user_id = user_id
        pass

    def get_last_played_tracks(self, limit=10):
        #limit: number of tracks received
        #returns list  of last played tracks
        url = f"https://api.spotify.com/v1/me/player/recently-played?limit={limit}"
        response = self._place_get_api_request(url)
        response_json = response.json()
        #tracks = [Track(track["name"], track["id"], track["artists"][0]["name"]) for
                #track in response_json["tracks"]]
        print(response_json)
        #return tracks

    def _place_get_api_request(self, url):
        response = requests.get(
            url, 
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.authorization_token}"
            }
        )
        return response
    def _place_post_api_request(self, url, data):
        response = requests.get(
            url,
            data = data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.authorization_token}"
            }
        )
        return response

    def get_track_recommendations(self, tracks, limit=10):
        #seed_tracks: track references for song recommendations
        #limit: number of tracks to be returned
        #returns recommended tracks
        seed_tracks_url = ""
        for track in tracks:
            seed_tracks_url += track.id + ","
        seed_tracks_url = seed_tracks_url[:-1]
        url = f"https://api.spotify.com/v1/recommendations?seed_tracks={seed_tracks_url}&limit={limit}"
        response = self._place_get_api_request(url)
        response_json = response.json()
        tracks = [Track(track["name"], track["id"], track["artists"][0]["name"]) for
                  track in response_json["tracks"]]

        return tracks

    def create_playlist(self, name, description, public):
        data = json.dumps({
            "name": name,
            "description": description,
            "public": public
        })
        url = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"
        response = self._place_post_api_request(url,data)
        response_json = response.json()

        #create playlist
        playlist_id = response_json["id"]
        playlist = Playlist(name, description, public, playlist_id)
        return playlist

    def add_songs_to_playlist(self, playlist, tracks):
        track_uris = [track.create_spotify_uri() for track in tracks]
        data = json.dumps(track_uris)
        url = f"https://api.spotify.com/v1/playlists/{playlist.id}/tracks"
        response = self._place_post_api_request(url,data)
        response_json = response.json()
        return response_json

