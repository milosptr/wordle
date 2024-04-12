from logic_layer.HistoryService import HistoryService
from logic_layer.UserScore import UserScore
from logic_layer.UserService import UserService


class ScoreBoard:
    def __init__(self):
        self.history_service = HistoryService()
        self.user_service = UserService()

    def get_score_board(self):
        history = self.history_service.get_history()
        user_scores = {}
        for game in history:
            user = self.user_service.get_user(game.user_id)
            score = game.score
            if user.get_id() not in user_scores:
                user_scores[user.get_id()] = UserScore(user.username, score)
            else:
                user_scores[user.get_id()].add_score(score)

        return sorted(user_scores.values(), key=lambda x: x.highest_score, reverse=True)

