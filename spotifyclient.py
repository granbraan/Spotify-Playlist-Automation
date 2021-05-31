import json
import requests

from track import Track
from playlist import Playlist

class SpotifyClient:
    #Performs varius tasks using Spotify Api""

    def __init__(self, authorization_token, user_id):
        self.authorization_token = authorization_token
        self.user_id = user_id
        pass

    def get_last_played_tracks(self, limit=10):

        url = f"https://api.spotify.com/v1/me/player/recently-played?limit=10"
        response = self._place_get_api_request(url)
        resonse_json = response.json()
        tracks = [Track(track["track"]["name"], track["track"]["id"], track["track"]["artist"][0]["name"]) 
        for track in response_json["items"]]
        return tracks

    def _place_get_api_request(self, url):
        response = requests.get(url, 
        headers={
            "Cotent-Type": "application/json",
            "OAuthorization": f"Token: {self.authorization_token}"
            }
        )
        return response
