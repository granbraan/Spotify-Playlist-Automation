import spotipy

class Playlist:
    """Playlist represents a Spotify playlist."""

    def __init__(self, name, description, public, id):
        """
        :param name (str): Playlist name
        :param id (int): Spotify playlist id
        :param descrption: optional description for Spotify playlist
        :param public: Public or Private spotify playlist
        """
        self.name = name
        self.description = description
        self.public = public
        self.id = id

    def __str__(self):
        return f"Playlist: {self.name}"