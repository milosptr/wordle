from common.constants import bcolors
from common.exceptions import WordUsedException, InvalidWordLengthException, InvalidLetterException
from common.state import State
from logic_layer.HistoryService import HistoryService
from logic_layer.WordBankService import WordBankService
from models.History import History
from utils.helpers import calculate_score


class Game:
    def __init__(self, level: int = 5, max_attempts: int = 6):
        self.__chosen_level = level
        self.__word_bank_service = WordBankService(level)
        self.__history_service = HistoryService()
        self.__word_bank = self.__word_bank_service.get_word_bank()
        self.__used_words_from_bank = []
        self.__used_words = []
        self.__used_letters = {}
        self.__current_word = self.select_random_word()
        self.__max_attempts = max_attempts
        self.__guesses = 0
        self.__word_guesses_positions = []

    # GETTERS
    def get_level(self) -> int:
        return self.__chosen_level

    def get_current_word(self) -> str:
        return self.__current_word

    def get_max_attempts(self) -> int:
        return self.__max_attempts

    def get_guesses(self):
        return self.__guesses

    def get_used_words(self):
        return self.__used_words

    def get_word_guesses_positions(self):
        return self.__word_guesses_positions

    def get_used_letters(self):
        return self.__used_letters

    def is_letter_used(self, letter: str) -> tuple:
        return self.__used_letters[letter.upper()] if letter.upper() in self.__used_letters else (None, None)

    # SETTERS
    def update_guesses(self):
        self.__guesses += 1

    def update_used_words(self, letter):
        self.__used_words.append(letter)

    def __validate_word(self, word: str):
        """Validate the word."""

        # Check if word is already used
        if word in self.__used_words:
            raise WordUsedException

        # Check if word is correct length
        if len(word) != self.__chosen_level:
            raise InvalidWordLengthException

        # Check if each letter is valid character (a-z)
        for letter in word:
            if not letter.isalpha():
                raise InvalidLetterException

    def save_game(self, result: str = 'win'):
        """Save the to the history."""
        game_state = State()
        if game_state.get_state('user') is not None:
            score = calculate_score(self.get_level(), result, self.get_max_attempts(), self.get_guesses())
            user_id = game_state.get_state('user').uuid
            history = History(None, user_id, self.get_current_word(), result, self.get_guesses(), score)
            self.__history_service.add_history(history)

    def guess_word(self, word: str):
        """Guess a word and return the result."""
        self.__validate_word(word)
        self.update_guesses()
        self.update_used_words(word)
        self.get_letter_positions(word)
        if word == self.__current_word:
            return True
        return False

    def get_letter_positions(self, word: str):
        """Get the positions of the letters in the word."""
        correct_positions = list(self.__current_word)
        guessed_positions = list(word)
        result = [bcolors.WHITE] * len(correct_positions)

        # First check for correct positions
        for i in range(len(correct_positions)):
            letter = guessed_positions[i].upper()
            if letter not in self.__used_letters:
                self.__used_letters[letter] = (False, False)
            if correct_positions[i] == guessed_positions[i]:
                result[i] = bcolors.OKGREEN
                correct_positions[i] = None
                self.__used_letters[letter] = (True, False)

        # Then check for correct letters in wrong positions
        for i in range(len(correct_positions)):
            letter = guessed_positions[i].upper()
            if guessed_positions[i] in correct_positions:
                result[i] = bcolors.WARNING
                correct_positions[correct_positions.index(guessed_positions[i])] = None
                self.__used_letters[letter] = (self.__used_letters[letter][0], True)
            elif result[i] != bcolors.OKGREEN:
                result[i] = bcolors.FAIL

        self.__word_guesses_positions.append(result)

    def select_random_word(self):
        """Selects a random word from the word bank."""
        random_word = self.__word_bank_service.get_random_word()

        # If the random word is already used, get a new random word
        if random_word in self.__used_words_from_bank:
            return self.select_random_word()

        self.__current_word = self.__word_bank_service.get_random_word()
        self.__used_words_from_bank.append(self.__current_word)
        return self.__current_word



