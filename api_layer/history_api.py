import json
from pathlib import Path

from models.History import History

class HistoryAPI:
    def __init__(self):
        self.history_file_path = Path(History.file_path)
        # Ensure the history file exists
        self.history_file_path.touch(exist_ok=True)

    def get_history(self, user_id=None) -> list[History]:
        """Retrieves the game history, optionally filtered by user ID."""
        try:
            with self.history_file_path.open('r', encoding='utf-8') as file:
                history_data = json.load(file)
        except json.JSONDecodeError:
            return []

        history = []
        # Pack the history into a list of History objects
        for game in history_data:
            history.append(History(
                game['uuid'],
                game['user_id'],
                game['word'],
                game['result'],
                game['guesses'],
                game['score'],
                game['timestamp']
            ))

        if user_id is not None:
            # Filter the history by user ID
            history = [game for game in history if str(game['user_id']) == str(user_id)]

        return history

    def add_history(self, new_entry: History):
        """Adds a game result to the history."""
        with self.history_file_path.open('r+', encoding='utf-8') as file:
            try:
                history = json.load(file)
            except json.JSONDecodeError:
                history = []

            # Append the new game result
            history.append(new_entry.get_json_format())

            # Move back to the start of the file to overwrite it
            file.seek(0)
            json.dump(history, file, indent=4)
            # Remove remaining parts of the old file
            file.truncate()




