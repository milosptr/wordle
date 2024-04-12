from models.User import User
from utils.printing import print_with_borders, print_separator_line


class State:
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        This method is used to implement the singleton pattern.
        """
        if cls._instance is None:
            cls._instance = super(State, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'is_initialized'):
            self.is_initialized = True
            self._state = {
                'user': None,
                'wins': 0,
                'losses': 0,
                'games_played': 0
            }

    def get_state(self, key) -> int | User:
        """Dynamically retrieves the value for the given state key."""
        return self._state.get(key, None)

    def set_state(self, key, value):
        """Dynamically sets the state key to the provided value."""
        if key in self._state and (isinstance(value, int) or isinstance(value, User)):
            self._state[key] = value
        else:
            print(f"Invalid key or value. Key must be one of {list(self._state.keys())} and value must be an integer.")

    def __str__(self):
        """Returns a string representation of the current state."""
        return f"State: {self._state}"

    def print_state(self):
        """Prints the current state."""
        if self.get_state('games_played') > 0:
            print_separator_line()
            print_with_borders(f"Games Played: {self.get_state('games_played')}", 'center')
            print_with_borders(f"Wins: {self.get_state('wins')}", 'center')
            print_with_borders(f"Losses: {self.get_state('losses')}", 'center')
        if self.get_state('user') is not None:
            print_with_borders(f"User: {self.get_state('user').name} ({self.get_state('user').username})", 'center')

    @staticmethod
    def test():
        """A simple test method to verify the functionality of the State class."""
        state = State()
        print(state)  # Initial state

        # Setting values
        state.set_state('games_played', 1)
        state.set_state('wins', 1)
        state.set_state('losses', 0)
        # set non-existing key to test error message
        state.set_state('random_key', 1)

        # Getting values
        assert state.get_state('games_played') == 1, "Games played should be 1"
        assert state.get_state('wins') == 1, "Wins should be 1"
        assert state.get_state('losses') == 0, "Losses should be 0"
        assert state.get_state('random_key') is None, "Random key should not exist"

        print('Games Played:', state.get_state('games_played'))
        print('Wins:', state.get_state('wins'))
        print('Losses:', state.get_state('losses'))

        print(state)

        print("Test passed!")

