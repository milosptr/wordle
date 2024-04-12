import json


class Navigation:
    """
    Navigation class is responsible for handling the navigation of the application
    """

    def __init__(self):
        with open('navigation.json', 'r', encoding='utf-8') as file:
            self.navigation_data = json.load(file)

    def get_specific_menu(self, state: str):
        """
        Returns the options for the current state.
        """
        return self.navigation_data.get(state, [])
