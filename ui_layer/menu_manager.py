from common.constants import bcolors
from ui_layer.navigation import Navigation
from ui_layer.views.game_ui import GameUI
from ui_layer.views.history_ui import HistoryUI
from ui_layer.views.score_board_ui import ScoreBoardUI
from ui_layer.views.user_ui import UserUI
from ui_layer.views.word_bank_ui import WordBankUI
from utils.printing import clear_screen, print_header, print_with_borders, print_menu_options, print_footer
from common.state import State


def exit_program():
    """
    This method is used to exit the program.
    """
    print('You have exited the program. Goodbye!')
    exit()


class MenuManager:
    """
    The MenuManager class is responsible for managing the menu.
    It keeps track of the current state of the menu and the menu stack.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        This method is used to implement the singleton pattern.
        """
        if cls._instance is None:
            cls._instance = super(MenuManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'is_initialized'):
            self.state = 'start'
            self.error_message = ''
            self.menu_stack = []
            self.game_state = State()
            self.is_initialized = True

    def get_state(self) -> str:
        """
        Returns the current state of the menu manager.
        """
        return self.state

    def set_state(self, state: str) -> None:
        """
        Sets the current state of the menu manager.
        Updates the menu stack accordingly.
        """
        if state != 'start':
            self.menu_stack.append(self.state)
            self.state = state
        else:
            self.state = 'start'
            self.menu_stack = []

        if self.menu_stack is None:
            self.menu_stack = []

    def get_error_message(self) -> str:
        """
        Returns the current error message.
        """
        return self.error_message

    def set_error_message(self, error_message: str) -> None:
        """
        Sets the current error message.
        """
        self.error_message = error_message

    def run(self):
        """
        This method runs the menu manager and displays the current menu.
        """
        options = Navigation().get_specific_menu(self.state)
        menu_options = list(map(lambda o: o['name'], options))
        if len(menu_options) > 0:
            page_title = self.state.replace('_', ' ').title()

            clear_screen()
            print_header()
            print_with_borders(page_title, 'center', color=bcolors.OKCYAN)
            print_menu_options(menu_options)
            self.game_state.print_state()
            print_footer(self.error_message)
            self.error_message = ''

            try:
                user_input = input('Select an option: ')
                if not self.handle_shortcuts(user_input):
                    try:
                        option_index = int(user_input) - 1
                        option = options[option_index] if option_index < len(options) else None
                        if 'next' in option:
                            self.set_state(option['next'])
                        else:
                            self.handle_user_selection(user_input)
                    except Exception as e:
                        print(e, 'error')
                        self.error_message = 'Invalid input'
            except KeyboardInterrupt:
                print('Goodbye!')
                exit_program()
        else:
            self.error_message = 'Invalid input'
            self.menu_stack = []
            self.set_state('start')

        self.run()

    def handle_user_selection(self, user_input: str) -> None:
        """
        This method is used to handle the user's selection.
        """

        match self.state:
            case 'start':
                match user_input:
                    case '1':
                        game = GameUI()
                        game.start_game()
                    case '2':
                        WordBankUI().view_add_word()
                    case '3':
                        ScoreBoardUI().view_score_board()
                    case '4':
                        HistoryUI().view_history()
                    case '6':
                        exit_program()
                    case _:
                        self.set_error_message('Invalid input. Please try again.')
                pass
            case 'user_management_menu':
                match user_input:
                    case '1':
                        UserUI().view_select_user()
                    case '2':
                        UserUI().view_create_user()
                    case _:
                        self.set_error_message('Invalid input. Please try again.')
            case _:
                pass

    def handle_shortcuts(self, user_input: str) -> bool:
        """
        Handles the shortcuts for the menu.
        """
        __is_shortcut = True
        if user_input.lower() in ['q', 'quit']:
            exit_program()
        elif user_input.lower() in ['b', 'back']:
            self.go_back()
        elif user_input.lower() == 'r':
            self.menu_stack = []
            self.set_state('start')
        else:
            __is_shortcut = False
        return __is_shortcut

    def go_back(self):
        """
        This method is used to go back to the previous menu.
        """
        if len(self.menu_stack) > 0:
            self.state = self.menu_stack.pop()
        else:
            self.state = 'start'
            self.menu_stack = []
