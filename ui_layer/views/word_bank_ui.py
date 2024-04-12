from common.constants import bcolors
from logic_layer.WordBankService import WordBankService
from utils.printing import clear_screen, print_separator_line, print_with_borders, print_vertical_space_with_borders, \
    print_with_centered_border, print_footer


class WordBankUI:
    def __init__(self):
        self.error_message = ''
        self.word = ''

    def print_add_word_screen(self, word=''):
        clear_screen()
        print_separator_line()
        print_with_borders('Create New User', 'center', color=bcolors.OKCYAN)
        print_separator_line()
        print_vertical_space_with_borders(4)
        print_with_centered_border(f'Your word: {word}', separator_char='')
        print_with_centered_border(f'Word length: {len(word)}', separator_char='')
        print_vertical_space_with_borders(4)
        print_with_borders('Allowed characters: A-Z and a-z', color=bcolors.WARNING)
        print_with_borders('Allowed length: 3-6 characters', color=bcolors.WARNING)
        print_footer(self.error_message, restart_option=False)
        self.error_message = ''

    def view_add_word(self):
        while self.word == '':
            self.print_add_word_screen()
            word = input("Enter a word: ")
            if word.lower() == 'q' or word.lower() == 'quit':
                exit(0)
            if word.lower() == 'b' or word.lower() == 'back':
                break
            if not word.isalpha() or not 3 <= len(word) <= 6:
                self.error_message = 'Word must be between 3-6 characters long and only contain letters A-Z and a-z. Please try again.'
                continue
            self.print_add_word_screen(word)
            user_input = input("Press enter to confirm or q/Q to abort adding word...")
            if user_input.lower() != 'q':
                self.word = word
                WordBankService(len(word)).add_word(word.upper())
                print(f"Word {word} has been added to the word bank.")
                input("Press enter to continue...")
            if user_input.lower() == 'q':
                break

