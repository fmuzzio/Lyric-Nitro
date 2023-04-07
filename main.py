


from src.dataprocessing import ScratchModelTextGenerator
from src.dataprocessing import GPT2ModelTextGenerator
from src.datacollection import APIHandler




class Main:
     def __init__(self, api_key):
        self.api_key = api_key
        self.api_handler = APIHandler(api_key)
     

     def musicData(self):
        artist_name = "Travis Scott"
        track_name = "Stargazing"
        input_text = "Don't you open up that window "

        lyrics = self.api_handler.fetch_lyrics(artist_name, track_name)
        return (lyrics, input_text)


     def gpt2Model(self):
         
         lyrics, input_text  = self.musicData()
         text_generator = GPT2ModelTextGenerator()

         if lyrics:
              generated_text = text_generator.generate_text(input_text)
              print(generated_text)
         else:
              print("Failed to fetch lyrics.")
     
     def scratchModel(self):

         lyrics, input_text  = self.musicData()

         if lyrics:
            text_generator = ScratchModelTextGenerator(lyrics)
            text_generator.train()
            generated_text = text_generator.generate_text(input_text)
            print(generated_text)
         else:
            print("Failed to fetch lyrics.")





if __name__ == '__main__':
    
    api_key = "your_api_key"  #enter your API key

    main = Main(api_key)
    #main.gpt2Model()
    main.scratchModel()





