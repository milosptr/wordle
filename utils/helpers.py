from datetime import datetime


def format_date(timestamp: str, format_output: str = "%Y-%m-%d %H:%M") -> str:
    """
    Format the date from isoformat to a human-readable format
    :param format_output: the format to output the date
    :param timestamp: isoformat timestamp
    :return: 'YYYY-MM-DD HH:MM' formatted timestamp
    """
    return datetime.fromisoformat(timestamp).strftime(format_output)


def calculate_score(word_len: int, status: str, total_attempts: int, actual_attempts: int, factor=10, penalty_factor=5) -> int:
    """
    Calculate the score based on the word length, total attempts, actual attempts, factor, and penalty factor.
    Factor is the base score multiplier.
    Penalty factor is the factor by which the score is reduced for each attempt.
    """
    if status == 'lose':
        return 0
    base_score = word_len * factor
    attempt_penalty = (total_attempts - actual_attempts) * penalty_factor
    total_score = base_score + attempt_penalty
    return total_score
