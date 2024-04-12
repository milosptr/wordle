from logic_layer.ScoreBoard import ScoreBoard
from utils.printing import print_table


class ScoreBoardUI:
    def __init__(self):
        self.score_board = ScoreBoard()

    def get_score_board(self):
        return self.score_board.get_score_board()

    def view_score_board(self):
        score_board = self.get_score_board()
        score_board = list(map(lambda s: s.get_list_of_values(), score_board))
        columns = ['User', 'Highest Score', 'Average Score']
        print_table(columns, score_board, 'Score Board')

        try:
            input("Press enter to go back...")
        except KeyboardInterrupt:
            print('\nGoodbye!')
            exit(0)

