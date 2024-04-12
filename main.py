from common.constants import bcolors
from ui_layer.menu_manager import MenuManager
from utils.printing import clear_screen, print_separator_line, print_with_borders, print_vertical_space_with_borders, \
    print_with_centered_border


def print_instructions():
    clear_screen()
    print_separator_line()
    print_with_borders('Instructions', 'center', color=bcolors.WARNING)
    print_separator_line()
    print_vertical_space_with_borders(4)
    print_with_centered_border(f'{bcolors.OKCYAN}Welcome to wordle!{bcolors.ENDC}', separator_char='')
    print_with_centered_border(f'{bcolors.WARNING}You are currently logged in as a guest user.{bcolors.ENDC}', separator_char='')
    print_with_centered_border(f'{bcolors.WARNING}You can play the game as a guest user, or you can create an account.{bcolors.ENDC}', separator_char='')
    print_with_centered_border(f'{bcolors.WARNING}If you are a guest user, your score will not be saved between sessions.{bcolors.ENDC}', separator_char='')
    print_with_centered_border(f'{bcolors.WARNING}Its advised to create an account to keep track of your score.{bcolors.ENDC}', separator_char='')
    print_vertical_space_with_borders(4)
    print_separator_line()


if __name__ == "__main__":
    print_instructions()
    try:
        input("Press enter to acknowledge the instructions...")
    except KeyboardInterrupt:
        print('\nGoodbye!')
        exit(0)
    menu_manager = MenuManager()
    menu_manager.run()

