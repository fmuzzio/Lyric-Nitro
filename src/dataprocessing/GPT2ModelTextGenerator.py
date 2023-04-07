import tensorflow as tf
from transformers import TFGPT2LMHeadModel, GPT2Tokenizer

class GPT2ModelTextGenerator:
    def __init__(self):
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        self.model = TFGPT2LMHeadModel.from_pretrained("gpt2")

    def generate_text(self, input_text, max_length=100):
        input_ids = self.tokenizer.encode(input_text, return_tensors="tf")
        
        # Check if max_length is greater than the input text length
        if max_length <= len(input_ids[0]):
            max_length = len(input_ids[0]) + 1

        generated_output = self.model.generate(input_ids, max_length=max_length, num_return_sequences=1)
        generated_text = self.tokenizer.decode(generated_output[0], skip_special_tokens=True)
        return generated_text
