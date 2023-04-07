import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


# this class uses a model that was created from scratch

class ScratchModelTextGenerator:
    def __init__(self, lyrics):
        self.data = lyrics
        self.tokenizer = Tokenizer()
        self.corpus = self.data.lower().split("\n")
        self.tokenizer.fit_on_texts(self.corpus)
        self.total_words = len(self.tokenizer.word_index) + 1
        self.input_sequences = self.prepare_input_sequences()
        self.max_sequence_len = max([len(x) for x in self.input_sequences])
        self.input_sequences = np.array(pad_sequences(self.input_sequences, maxlen=self.max_sequence_len, padding='pre'))
        self.xs, self.ys = self.prepare_data()
        self.model = self.build_model()

    def prepare_input_sequences(self):
        input_sequences = []
        for line in self.corpus:
            token_list = self.tokenizer.texts_to_sequences([line])[0]
            for i in range(1, len(token_list)):
                n_gram_sequence = token_list[:i + 1]
                input_sequences.append(n_gram_sequence)
        return input_sequences

    def prepare_data(self):
        xs = self.input_sequences[:, :-1]
        labels = self.input_sequences[:, -1]
        ys = tf.keras.utils.to_categorical(labels, num_classes=self.total_words)
        return xs, ys

    def build_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Embedding(self.total_words, 64, input_length=self.max_sequence_len - 1),
            tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(150)),
            tf.keras.layers.Dense(self.total_words, activation='softmax')
        ])

        model.compile(loss='categorical_crossentropy', optimizer=tf.keras.optimizers.Adam(lr=0.01), metrics=['accuracy'])
        return model


    def train(self, epochs=100, verbose=1):
        self.model.fit(self.xs, self.ys, epochs=epochs, verbose=verbose)


    def generate_text(self, seed_text, num_generated_words = 50):
       

        for _ in range(num_generated_words):
            token_list = self.tokenizer.texts_to_sequences([seed_text])[0]
            token_list = pad_sequences([token_list], maxlen=self.max_sequence_len - 1, padding='pre')
            
            # Use 'predict' method and 'argmax' to get the class with the highest probability
            probabilities = self.model.predict(token_list, verbose=0)
            predicted = np.argmax(probabilities, axis=-1)
            
            output_word = ""

            for word, index in self.tokenizer.word_index.items():
                if index == predicted:
                    output_word = word
                    break

            seed_text += " " + output_word

        return seed_text

