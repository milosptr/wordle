from api_layer.history_api import *
from models import History
from utils.helpers import format_date


class HistoryService:
    """
    The HistoryService class is responsible for handling the game history.
    It uses the HistoryAPI class to interact with the history file.
    """
    def __init__(self):
        self.history_dao = HistoryAPI()

    def get_history(self):
        """Retrieves the game history."""
        return self.history_dao.get_history()

    def get_user_history(self, user_id):
        """Retrieves the game history for a specific user."""
        return self.history_dao.get_history(user_id)

    def get_highest_score_for_each_user(self):
        """
        Retrieves the highest score for each user.
        :return: list[dict]
        """
        history = self.get_history()
        user_scores = {}
        for game in history:
            user_id = game.user_id
            score = game.score
            if user_id not in user_scores or score > user_scores[user_id]['score']:
                user_scores[user_id] = {
                    'score': score,
                    'game': game.uuid,
                    'timestamp': game.timestamp
                }

        highest_scores = []
        for user_id, data in user_scores.items():
            highest_scores.append({
                'user_id': user_id,
                'score': data['score'],
                'game': data['game'],
                'timestamp': format_date(data['timestamp'])
            })

        return highest_scores

    def add_history(self, history: History):
        """Adds a game result to the history."""
        if not (history, History.__class__):
            raise ValueError("The history must be an instance of the History class.")
        self.history_dao.add_history(history)
