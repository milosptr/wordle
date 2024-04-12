from datetime import datetime
from uuid import uuid4

from logic_layer.UserService import UserService
from utils.helpers import format_date


class History:
    """
    The History model class
    """
    database = 'history.json'
    file_path = f'data_layer/repository/{database}'

    def __init__(self, uuid: str | None, user_id: int, word: str, result: str, guesses: int, score: float, timestamp: str | None = None):
        self.uuid = uuid if uuid is not None else uuid4()
        self.user_id = user_id
        self.word = word
        self.guesses = guesses
        self.result = result  # win or lose
        self.score = score
        self.timestamp = timestamp if timestamp is not None else format_date(datetime.now().isoformat())

    def __str__(self):
        return f"{self.word} - {self.score} - {self.timestamp}"

    def __getitem__(self, item):
        """
        Get the item from the history
        """
        return self.__dict__[item]

    def get_list_of_values(self):
        """
        Get the list of values from the history
        """
        return self.__dict__.values()

    def get_table_list_of_values(self):
        """
        Get the list of values from the history for the table
        """
        username = UserService().get_user(self.user_id).username
        return [
            username,
            self.word,
            self.guesses,
            self.result,
            self.score,
            self.timestamp
        ]

    def get_json_format(self):
        """
        Get the history in JSON format
        :return: dict
        """
        return {
            'uuid': str(self.uuid),
            'user_id': str(self.user_id),
            'word': self.word,
            'guesses': self.guesses,
            'result': self.result,  # 'win' or 'lose'
            'score': self.score,
            'timestamp': self.timestamp
        }



