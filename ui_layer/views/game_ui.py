from common.constants import bcolors, DEFAULT_LEVEL, DEFAULT_MAX_ATTEMPTS
from common.exceptions import ShouldRestartException, WordUsedException, InvalidWordLengthException, \
    InvalidLetterException, WordGuessedException, ShouldGoBackException
from common.state import State
from logic_layer.Game import Game
from utils.printing import (clear_screen,
                            print_with_centered_border, print_with_borders,
                            print_vertical_space_with_borders,
                            print_separator_line, print_footer, print_boxes)


class GameUI:
    def __init__(self):
        self.level = None
        self.max_attempts = None
        self.keyboard = [
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
        ]
        self.error_message = ''
        self._game_state = State()

    def __restart_game(self):
        """Resets or initializes the game settings."""
        self.level = None
        self.max_attempts = None
        self.start_game()

    def __print_level_and_attempts(self):
        """Prints the current level and max attempts, handling defaults."""
        level = f'{DEFAULT_LEVEL} (Default)' if self.level is None else self.level
        attempts = f'{DEFAULT_MAX_ATTEMPTS} (Default)' if self.max_attempts is None else self.max_attempts

        clear_screen()
        print_separator_line()
        print_with_borders('Choose level and attempts', 'center', color=bcolors.OKCYAN)
        print_separator_line()
        print_vertical_space_with_borders(4)
        print_with_centered_border(f'Chosen level: {level}', separator_char='')
        print_with_centered_border(f'Max attempts: {attempts}', separator_char='')
        print_vertical_space_with_borders(4)
        print_footer(self.error_message)
        self.error_message = ''

    def __print_wordle(self, wordle: Game, positions: list, game_over: bool = False):
        """Prints the wordle game state."""
        used_words = wordle.get_used_words()
        clear_screen()
        print_separator_line()
        print_with_borders('Wordle', 'center', color=bcolors.OKCYAN)
        print_separator_line()
        print_vertical_space_with_borders(4)
        for attempt in range(wordle.get_max_attempts()):
            attempt_positions = positions[attempt] if attempt < len(positions) else []
            # if there is a used word for this attempt, print it
            if attempt < len(used_words):
                print_boxes(used_words[attempt], attempt_positions)
            else:
                print_boxes(" " * wordle.get_level())
        print_vertical_space_with_borders(2)

        for row in self.keyboard:
            marked_letters = []
            for letter in row:
                if wordle.is_letter_used(letter) != (None, None):
                    if wordle.is_letter_used(letter)[0]:
                        marked_letters.append(bcolors.OKGREEN + letter + bcolors.ENDC)
                    elif wordle.is_letter_used(letter)[1]:
                        marked_letters.append(bcolors.WARNING + letter + bcolors.ENDC)
                    else:
                        marked_letters.append(bcolors.FAIL + letter + bcolors.ENDC)
                else:
                    marked_letters.append(letter)
            print_with_borders(' '.join(marked_letters), 'center')

        print_vertical_space_with_borders(1)

        if game_over:
            self._game_state.set_state('games_played', self._game_state.get_state('games_played') + 1)
            self._game_state.set_state('losses', self._game_state.get_state('losses') + 1)
            print_with_borders(bcolors.FAIL + 'Game over! The correct word is:' + bcolors.ENDC, 'center')
            print_boxes(wordle.get_current_word(), [bcolors.LIGHT_PURPLE] * wordle.get_level())

        print_vertical_space_with_borders(2)
        self._game_state.print_state()
        print_footer(self.error_message)

    def __handle_shortcuts_and_validate(self, option: str, min_val: int, max_val: int) -> bool:
        """Handles shortcuts and validates the input, raising exceptions as needed."""
        if option.lower() == 'q':
            exit()
        if option.lower() == 'r':
            raise ShouldRestartException
        if option.lower() == 'b':
            raise ShouldGoBackException
        if option != '' and not option.isdigit():
            self.error_message = 'Invalid input. Please enter a valid number!'
            return False
        if option != '' and (int(option) < min_val or int(option) > max_val):
            self.error_message = f'Invalid input. Please choose a value between {min_val} and {max_val}!'
            return False
        return True

    def __choose_setting(self, prompt: str, default: int, min_val: int, max_val: int) -> int:
        """Generic method for choosing a setting like level or max attempts."""
        self.__print_level_and_attempts()
        value = input(prompt)

        # if the input is invalid, show an error message and ask again
        if not self.__handle_shortcuts_and_validate(value, min_val, max_val):
            return self.__choose_setting(prompt, default, min_val, max_val)

        return int(value) if value else default

    @staticmethod
    def __end_of_the_game():
        """Handles the end of the game logic."""
        user_choice = input('Press Enter to restart the game or q/Q to quit: ').upper()
        if user_choice == '':
            raise ShouldRestartException

    def start_game(self):
        """Handles the game start logic, including level and attempts selection."""
        try:
            self.level = self.__choose_setting(
                'Choose a level between 3 and 6 (default is 5) or press Enter to skip: ',
                DEFAULT_LEVEL, 3, 6
            )
            self.max_attempts = self.__choose_setting(
                'Choose max attempts between 1 and 20 (default is 6) or press Enter to skip: ',
                DEFAULT_MAX_ATTEMPTS, 1, 20
            )
            self.__print_level_and_attempts()
            input('Press Enter to start the game...')

            # Start the game
            wordle = Game(self.level, self.max_attempts)
            while wordle.get_guesses() < wordle.get_max_attempts():
                try:
                    self.__print_wordle(wordle, wordle.get_word_guesses_positions())
                    user_input = input('Enter a word: ').upper()
                    if user_input == 'Q':
                        exit()
                    if user_input == 'R':
                        raise ShouldRestartException
                    if wordle.guess_word(user_input):
                        self.__print_wordle(wordle, wordle.get_word_guesses_positions())
                        wordle.save_game()
                        self._game_state.set_state('games_played', self._game_state.get_state('games_played') + 1)
                        self._game_state.set_state('wins', self._game_state.get_state('wins') + 1)
                        raise WordGuessedException
                except InvalidWordLengthException:
                    self.error_message = f'Invalid word length. Please enter a {self.level}-letter word.'
                except InvalidLetterException:
                    self.error_message = 'Invalid letter. Please enter a word with only letters (a-z).'
                except WordUsedException:
                    self.error_message = 'Word already used. Try another word!'

            # Game over
            wordle.save_game('lose')
            self.__print_wordle(wordle, wordle.get_word_guesses_positions(), True)
            self.__end_of_the_game()

        except WordGuessedException:
            print('Congratulations! You guessed the word!')
            self.__end_of_the_game()

        except ShouldRestartException:
            print('Restarting game...')
            self.__restart_game()

        except ShouldGoBackException:
            return

        except KeyboardInterrupt:
            print('Goodbye!')
            exit()
