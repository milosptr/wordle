class UserScore:
    def __init__(self, user: str, score: float):
        self.user = user
        self.highest_score = score
        self.scores = [score]

    def add_score(self, score: float):
        if score > self.highest_score:
            self.highest_score = score
        self.scores.append(score)

    def get_average_score(self):
        return round(sum(self.scores) / len(self.scores), 2)

    def get_list_of_values(self):
        return [self.user, self.highest_score, self.get_average_score()]
