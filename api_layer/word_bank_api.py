import json
from pathlib import Path
from random import randrange


class WordBankAPI:
    def __init__(self, word_len) -> None:
        self.word_len = word_len
        self.user_file_path = Path(f"data_layer/repository/word_bank/{self.word_len}_letter_words.json")
        # Ensure the user file exists
        self.user_file_path.touch(exist_ok=True)

    def get_word_bank(self):
        """Retrieves a word bank by word length."""
        try:
            with self.user_file_path.open('r', encoding='utf-8') as file:
                word_bank = json.load(file)
        except json.JSONDecodeError:
            return None

        return list(map(lambda w: w.upper(),word_bank))

    def get_random_word(self):
        """Retrieves a random word from the word bank."""
        word_bank = self.get_word_bank()
        if word_bank is None:
            return None

        random_index = randrange(len(word_bank))
        return word_bank[random_index]

    def add_word(self, word: str):
        """Adds a new word to the word bank."""
        with self.user_file_path.open('r+', encoding='utf-8') as file:
            try:
                word_bank = json.load(file)
            except json.JSONDecodeError:
                word_bank = []

            word_bank = list(map(lambda w: w.upper(), word_bank))

            # Check if the word already exists
            if word.upper() in word_bank:
                raise ValueError(f"Word {word.upper()} already exists in the word bank.")

            # Append the new word
            word_bank.append(word.upper())

            # Move back to the start of the file to overwrite it
            file.seek(0)
            json.dump(word_bank, file, indent=4)
            file.truncate()
