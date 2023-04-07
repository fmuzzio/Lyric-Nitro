import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
import json
import re

class APIHandler:
    def __init__(self, api_key):
        self.api_key = api_key


    def get_song_urls_from_data(self,data, artist_name):

        song_urls = []

        for hit in data["response"]["hits"]:
            if artist_name.lower() in hit["result"]["primary_artist"]["name"].lower():
                song_urls.append(hit["result"]["url"])

        return song_urls


    def fetch_lyrics(self, artist_name, track_name):
        url = f"https://api.genius.com/search?q={artist_name} {track_name}&access_token={self.api_key}"
        response = requests.get(url)
        data = json.loads(response.text)

        if response.status_code == 200:
            song_urls = self.get_song_urls_from_data(data, artist_name)

            if song_urls:
                for lyrics_url in song_urls:
                    lyrics_response = requests.get(lyrics_url)

                    if lyrics_response.status_code == 200:
                        soup = BeautifulSoup(lyrics_response.content, "html.parser")
                        lyrics_div = soup.find("div", class_=re.compile("^Lyrics__Root-"))

                        if lyrics_div:
                            lyrics = lyrics_div.get_text()
                            return lyrics.strip()
                        else:
                            print("Lyrics not found")
                            return None
                    else:
                        print("Failed to fetch lyrics")
                        return None
            else:
                print("Song not found")
                return None
        else:
            print("Failed to fetch song information")
            return None

