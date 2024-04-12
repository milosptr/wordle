from common.state import State
from logic_layer.HistoryService import HistoryService
from utils.printing import clear_screen, print_header, print_footer, print_with_centered_border, \
    print_separator_line_for_centered_border, print_table


class HistoryUI:
    def __init__(self):
        self.history_service = HistoryService()
        self.__game_state = State()

    def view_history(self):
        if self.__game_state.get_state('user') is not None:
            print(f"Game history for user: {self.__game_state.get_state('user').get_id()}")
            history = self.history_service.get_user_history(self.__game_state.get_state('user').get_id())
        else:
            history = self.history_service.get_history()

        history = list(map(lambda h: h.get_table_list_of_values(), history))
        columns = ['User', 'Word', 'Guesses', 'Result', 'Score', 'Date']
        print_table(columns, history, 'Game History')

        try:
            input("Press enter to go back...")
        except KeyboardInterrupt:
            print('\nGoodbye!')
            exit(0)
