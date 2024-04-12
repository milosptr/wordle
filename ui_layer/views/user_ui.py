from common.constants import bcolors
from common.state import State
from logic_layer.UserService import UserService
from models.User import User
from utils.printing import print_table, clear_screen, print_separator_line, print_with_borders, \
    print_vertical_space_with_borders, print_with_centered_border, print_footer


class UserUI:
    def __init__(self):
        self.__user_service = UserService()
        self.__game_state = State()
        self.error_message = ''

    def view_users(self):
        users = self.__user_service.get_users()
        columns = ['id', 'username', 'name']
        print_table(columns, map(lambda u: u.get_list_of_values(), users), 'Available Users')

    def view_select_user(self):
        self.view_users()
        selected_user = input("Select user by entering the ID/username of the user (enter to abort):")
        user = self.__user_service.get_user(selected_user)
        print(f"Selected user: {user.name} ({user.username})")
        try:
            user_input = input("Press enter to continue or q/Q to abort selecting user...")
            if user_input.lower() != 'q':
                self.__game_state.set_state('user', user)
        except KeyboardInterrupt:
            print('\nGoodbye!')
            exit(0)

    def print_create_user(self, username='', name=''):
        clear_screen()
        print_separator_line()
        print_with_borders('Create New User', 'center', color=bcolors.OKCYAN)
        print_separator_line()
        print_vertical_space_with_borders(4)
        print_with_centered_border(f'Username: {username}', separator_char='')
        print_with_centered_border(f'Name: {name}', separator_char='')
        print_vertical_space_with_borders(4)
        print_footer(self.error_message, back_option=False)
        self.error_message = ''

    def view_create_user(self):
        self.print_create_user()
        username = input("Enter a username: ")
        self.print_create_user(username)
        name = input("Enter your name: ")
        self.print_create_user(username, name)
        try:
            user_input = input("Press enter to confirm or q/Q to abort creating user...")
        except KeyboardInterrupt:
            print('\nGoodbye!')
            exit(0)
        if user_input.lower() != 'q':
            user = User(None, name, username)
            self.__user_service.add_user(user)
            print(f"User {name} ({username}) has been created.")
            self.__game_state.set_state('user', user)
