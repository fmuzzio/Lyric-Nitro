from src.textgenerator import TextGenerator
from src.api_handler import APIHandler

if __name__ == '__main__':
    api_handler = APIHandler()

    artist_name = "Travis Scott"
    track_name = "Stargazing"

    lyrics = api_handler.fetch_lyrics(artist_name, track_name)
    if lyrics:
        text_generator = TextGenerator(lyrics)
        text_generator.train(epochs=100, verbose=1)
        generated_text = text_generator.generate_text("Don't you open up that window ")
        print(generated_text)
    else:
        print("Failed to fetch lyrics.")

