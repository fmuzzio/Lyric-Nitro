import requests


class APIHandler:
    def __init__(self):
        self.base_url = "https://api.lyrics.ovh/v1/"

    def fetch_lyrics(self, artist_name, track_name):
        url = f"{self.base_url}{artist_name}/{track_name}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data["lyrics"]
        else:
            return None

