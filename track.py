import spotipy

class Track:
    #Represents parts of songs on Spotify

    def __init__(self, name, id, artist):
        self.name = name
        self.id = id
        self.artist = artist
        pass

    def create_spotify_uri(self):
        return f"spotify:track:{self.id}"

    def __str__(self):
        return f"{self.name} by {self.artist}"
        pass
