
from api_layer.word_bank_api import WordBankAPI


class WordBankService:
    def __init__(self, word_len: int):
        self.word_len = word_len
        self.word_bank_dao = WordBankAPI(word_len)

    def get_word_bank(self):
        """Retrieves the word bank."""
        return self.word_bank_dao.get_word_bank()

    def add_word(self, word: str):
        """Adds a new word to the word bank."""
        self.word_bank_dao.add_word(word)

    def get_random_word(self):
        """Retrieves a random word from the word bank."""
        return self.word_bank_dao.get_random_word()

