class WordBank:
    def __init__(self, word: str, length: int):
        self.word = word
        self.length = length

    def __str__(self):
        return f"{self.word}"
