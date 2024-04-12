import shutil
from common.constants import DEFAULT_WIDTH, DEFAULT_HEIGHT, DEFAULT_ALIGN, MAX_COLUMN_WIDTH
from common.constants import DEFAULT_PADDING_LEFT, DEFAULT_PADDING_RIGHT, DEFAULT_PADDING_SPACE
from common.constants import HEADER_HEIGHT, FOOTER_HEIGHT, TOTAL_PADDING, DEFAULT_BORDER, bcolors


def get_terminal_dimensions():
    """
    Get the dimensions of the terminal window.

    Returns:
        tuple: A tuple (width, height) representing the terminal dimensions.
    """
    terminal_size = shutil.get_terminal_size(fallback=(DEFAULT_WIDTH,
                                                       DEFAULT_HEIGHT))
    return terminal_size.columns, terminal_size.lines


def calculate_padding(text_length,
                      total_width,
                      padding_left=0,
                      padding_right=0):
    """
    Calculate the amount of padding needed to align text within the terminal.

    Args:
        text_length (int): The length of the text to be printed.
        total_width (int): The total width of the terminal.
        padding_left (int): Optional; additional padding to be added to the left.
        padding_right (int): Optional; additional padding to be added to the right.

    Returns:
        int: The amount of padding required.
    """
    return max(0, (total_width - text_length - padding_left - padding_right))


def calculate_text_length(text):
    """
    Calculate the length of the text to be printed.

    Args:
        text (str): The text to be printed.

    Returns:
        int: The length of the text without any color codes or escape sequences.
    """
    if bcolors.ENDC in text:
        return len(text) - (text.count(bcolors.ENDC) * 9)
    return len(text)


def clear_screen():
    """
    Clear the terminal screen.
    """
    # print("\x1b[1J\x1b[H", end="")
    print("\x1b[2J\x1b[H", end="")


def print_menu_options(options):
    """
    Print a list of menu options within the terminal.

    Args:
        options (list): A list of menu options to be printed.
    """
    width, height = get_terminal_dimensions()
    third_width = width // 3 + TOTAL_PADDING
    height = (height - HEADER_HEIGHT - FOOTER_HEIGHT - len(options) - 2) // 2

    print_vertical_space_with_borders(height=height)
    print_separator_line_for_centered_border(custom_width=third_width)
    for index, option in enumerate(options):
        print_with_centered_border(f"{index + 1}. {option}")
    print_separator_line_for_centered_border(custom_width=third_width)
    print_vertical_space_with_borders(height=height)


def print_vertical_space_with_borders(height=DEFAULT_HEIGHT):
    """
    Print vertical space within the terminal with borders.
    """
    for _ in range(height):
        print_with_borders()


def print_with_borders(text='',
                       align=DEFAULT_ALIGN,
                       padding_left=DEFAULT_PADDING_LEFT,
                       padding_right=DEFAULT_PADDING_RIGHT,
                       color=bcolors.WHITE):
    """
    Print text within the terminal with borders and aligned as specified.

    Args:
        text (str): The text to be printed.
        align (str): Optional; The alignment of the text ('left', 'right', 'center').
        padding_left (int): Optional; The padding to be added to the left of the text.
        padding_right (int): Optional; The padding to be added to the right of the text.
        color (str): Optional; The color of the text.
    """
    width, _ = get_terminal_dimensions()
    padding = calculate_padding(calculate_text_length(text), width,
                                padding_left, padding_right)
    outline_symbol = f'{bcolors.WHITE}=={bcolors.ENDC}'
    text = f'{color}{text}{bcolors.ENDC}'

    if align == 'right':
        formatted_text = f"{outline_symbol}{' ' * DEFAULT_PADDING_SPACE}{' ' * padding}{text}{' ' * DEFAULT_PADDING_SPACE}{outline_symbol}"
    elif align == 'center':
        left_padding = padding // 2
        right_padding = padding - left_padding
        formatted_text = f"{outline_symbol}{' ' * DEFAULT_PADDING_SPACE}{' ' * left_padding}{text}{' ' * right_padding}{' ' * DEFAULT_PADDING_SPACE}{outline_symbol}"
    else:
        formatted_text = f"{outline_symbol}{' ' * DEFAULT_PADDING_SPACE}{text}{' ' * padding}{' ' * DEFAULT_PADDING_SPACE}{outline_symbol}"

    print(formatted_text)


def print_separator_line_for_centered_border(char=DEFAULT_BORDER,
                                             custom_width=None):
    """
    Print a separator line across the terminal. Used for centered borders.
    """
    width, _ = get_terminal_dimensions()
    third_width = width // 3 + TOTAL_PADDING
    width = custom_width if custom_width else third_width
    print_with_borders(char * width, 'center')


def print_with_centered_border(text,
                               padding_left=DEFAULT_PADDING_LEFT,
                               padding_right=DEFAULT_PADDING_RIGHT,
                               separator_char=DEFAULT_BORDER):
    """
    Print text within the terminal with borders and aligned as specified.

    Args:
        text (str): The text to be printed.
        padding_left (int): Optional; The padding to be added to the left of the text.
        padding_right (int): Optional; The padding to be added to the right of the text.
        separator_char (str): Optional; The character to be used for the separator line.
    """
    width, _ = get_terminal_dimensions()
    third_width = width // 3
    formatted_text = f"{separator_char * 2}{' ' * padding_left}{text : <{third_width}}{' ' * padding_right}{separator_char * 2}"

    print_with_borders(formatted_text, 'center')


def print_separator_line(char=DEFAULT_BORDER):
    """
    Print a separator line across the terminal.

    Args:
        char (str): Optional; The character to be used for the separator line.
    """
    width, _ = get_terminal_dimensions()
    print(char * width)


def print_two_columns(left_text, right_text, padding_left=4, padding_right=4, left_length=None, right_length=None):
    """
    Print two columns of text within the terminal.

    Args:
        left_text (str): The text for the left column.
        right_text (str): The text for the right column.
        padding_left (int): Optional; The padding to be added to the left of the left column.
        padding_right (int): Optional; The padding to be added to the right of the right column.
        left_length (int): Optional; The length of the left text.
        right_length (int): Optional; The length of the right text.
    """
    width, _ = get_terminal_dimensions()
    left_text_len = left_length if left_length else calculate_text_length(left_text)
    right_text_len = right_length if right_length else calculate_text_length(right_text)
    padding = calculate_padding(
        left_text_len + right_text_len,
        width, padding_left, padding_right)

    empty_space = " " * padding
    print(
        f"=={' ' * DEFAULT_PADDING_SPACE}{left_text}{empty_space}{right_text}{' ' * DEFAULT_PADDING_SPACE}=="
    )


def print_header():
    """
    Print the header of the program with the name of the program.
    """
    header_text = [
        "db   d8b   db  .d88b.  d8888b. d8888b. db      d88888b",
        "88   I8I   88 .8P  Y8. 88  `8D 88  `8D 88      88.    ",
        "88   I8I   88 88    88 88oobY' 88   88 88      88ooooo",
        "Y8   I8I   88 88    88 88`8b   88   88 88      8800000",
        "`8b d8'8b d8' `8b  d8' 88 `88. 88  .8D 88booo. 88.    ",
        "  `8b8' `8d8'   `Y88P'  88   YD Y8888D' Y88888P Y88888P "
    ]
    print_separator_line()
    for line in header_text:
        print_with_borders(line, 'center', color=bcolors.KINDA_PURPLE)
    print_separator_line()


def print_footer(error=None, back_option=True, quit_option=True, restart_option=True):
    """
    Print the footer of the program with the available navigation options.

    Args:
        error (str): Optional; An error message to be displayed.
    """
    print_separator_line()
    print_with_borders()
    print_with_borders()
    go_back = f'{bcolors.BOLD}{bcolors.WARNING}[B]{bcolors.ENDC}{bcolors.ENDC} to go back /' if back_option else ''
    quit_program = f'{bcolors.BOLD}{bcolors.WARNING}[Q]{bcolors.ENDC}{bcolors.ENDC} to quit program /' if quit_option else ''
    restart = f'{bcolors.BOLD}{bcolors.WARNING}[R]{bcolors.ENDC}{bcolors.ENDC} to go to the beginning' if restart_option else ''
    go_back_len = 16 if back_option else 0
    quit_program_len = 21 if quit_option else 0
    restart_len = 26 if restart_option else 0
    # Calculate the length of the left shortcuts + 2 for the spaces
    left_shortcuts_len = go_back_len + quit_program_len + restart_len + 2


    left_shortcuts = f'{go_back} {quit_program} {restart}'

    print_two_columns(left_shortcuts, '', left_length=left_shortcuts_len)
    print_with_borders()
    if error:
        print_with_borders(f'Error: {error}', 'left', color=bcolors.BGFAIL)
    else:
        print_with_borders()
    print_separator_line()


def print_table(columns: [str], rows: [[str]], title: str = ''):
    """
    Print a table with the given columns and rows.
    """
    width, _ = get_terminal_dimensions()

    column_width = width // len(columns) - (DEFAULT_PADDING_LEFT + DEFAULT_PADDING_RIGHT)
    if column_width > MAX_COLUMN_WIDTH:
        column_width = MAX_COLUMN_WIDTH
    table_width = (column_width * len(columns) + 6)

    clear_screen()
    print_separator_line()
    print_vertical_space_with_borders(2)
    print_with_borders(f'{title.upper()}', 'center', color=bcolors.OKCYAN)
    print_vertical_space_with_borders(1)
    print_with_borders('=' * table_width, 'center')
    header = ['']
    for column in columns:
        column = column.replace('_', ' ')
        header.append(f'{column.title():^{column_width}}')
    header.append('')
    print_with_borders('+'.join(header), 'center', color=bcolors.LIGHT_PURPLE)
    print_with_borders('=' * table_width, 'center')

    for row in rows:
        row_data = ['']
        for column in row:
            row_data.append(f'{column:^{column_width}}')
        row_data.append('')
        print_with_borders('+'.join(row_data), 'center')
        print_with_borders('-' * table_width, 'center')

    print_vertical_space_with_borders(3)
    print_separator_line()


def print_boxes(word: str, colors: list[str] = None) -> None:
    """
    Print a word with each letter in a box. Each box will have a border and a color.
    :param word: word to print
    :param colors: list of colors for each letter
    :return:
    """
    # Define the size of the box around each letter
    box_size = 3  # This includes the borders
    total_box_width = (box_size + 2) * len(word)  # +2 for the left and right edges of each box
    terminal_width, _ = get_terminal_dimensions()

    # Calculate left padding to center the boxes
    left_padding = max(0, (terminal_width - total_box_width) // 2) - 4

    # Ensure the list of colors matches the length of the word
    # If not, set all colors to white
    if colors is None or len(word) != len(colors):
        colors = [bcolors.WHITE] * len(word)

    # Function to print a single line of boxes
    def print_line(content, is_border=False):
        # Apply left padding
        print('==' + ' ' * left_padding, end='')
        for letter, color in zip(word, colors):
            if is_border:
                print(color + content + bcolors.ENDC, end=' ')
            else:
                padding = ' ' * ((box_size - 1) // 2)
                middle = '|' + padding + letter + padding
                if box_size % 2 == 0:
                    middle += ' '
                middle += '|'
                print(color + middle + bcolors.ENDC, end=' ')
        # Apply right padding
        print(' ' * left_padding + '==')

    # Calculate the components of the box
    top_bottom_border = '+' + '-' * box_size + '+'

    # Print the top borders for all letters
    print_line(top_bottom_border, is_border=True)

    # Print the middle part for each letter
    print_line('', is_border=False)

    # Print the bottom borders for all letters
    print_line(top_bottom_border, is_border=True)


