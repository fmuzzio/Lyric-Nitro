import requests

class APIHandler:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.musixmatch.com/ws/1.1/"

    def fetch_lyrics(self, artist_name, track_name):
        payload = {
            "apikey": self.api_key,
            "q_artist": artist_name,
            "q_track": track_name,
            "format": "json"
        }
        response = requests.get(self.base_url + "matcher.lyrics.get", params=payload)
        data = response.json()

        if data["message"]["header"]["status_code"] == 200:
            return data["message"]["body"]["lyrics"]["lyrics_body"].replace("\n...\n\n******* This Lyrics is NOT for Commercial use *******", "").strip()
        else:
            return None
