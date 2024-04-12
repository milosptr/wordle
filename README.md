# Worlde

Wordle gives players six chances to guess a randomly selected five-letter word. The word level can be changed between 3, 4, 5, and 6 letter words, as well as number of chances you have.

## Features

- User Management: Create, retrieve users.
- Game History: Retrieve game history, optionally filtered by user ID, and add game results to the history.
- Word Bank: Retrieve a word bank by word length, retrieve a random word from the word bank, and add new words to the word bank.

## Requirements

- Python 3.8 or higher

## Run the application
```python main.py```

## Project Structure

Below is an overview of the key components of the project structure:

### API Layer

- `api_layer/`
    - `history_api.py`: API endpoints for handling history-related operations.
    - `user_api.py`: API endpoints for user management.
    - `word_bank_api.py`: API endpoints for accessing the word bank.

### Common Utilities

- `common/`
    - `constants.py`: Defines constants used across the application.
    - `exceptions.py`: Custom exceptions for the application.
    - `state.py`: Shared state information across the application.

### Data Layer

- `data_layer/`
    - `repository/`: Contains JSON files used as a simple data store.
        - `history.json`: Stores game history data.
        - `users.json`: Stores user data.
        - `word_bank/`: Different JSON files for word banks of various lengths.

### Logic Layer

- `logic_layer/`
    - `Game.py`: Core game logic.
    - `HistoryService.py`: Business logic for history tracking.
    - `ScoreBoard.py`: Logic for managing scores.
    - `UserService.py`: Business logic for user management.
    - `WordBankService.py`: Logic for word bank operations.

### Models

- `models/`
    - `History.py`: Data model for game history.
    - `User.py`: Data model for user.
    - `WordBank.py`: Data model for word bank.

### UI Layer

- `ui_layer/`
    - `menu_manager.py`: Manages the main menu UI.
    - `navigation.py`: Handles navigation in the UI.
    - `views/`: Contains individual views for different UI components.
        - `game_ui.py`: UI for game interactions.
        - `history_ui.py`: UI for displaying game history.
        - `score_board_ui.py`: UI for the scoreboard.
        - `user_ui.py`: UI for user management.
        - `word_bank_ui.py`: UI for word bank display.

### Utils

- `utils/`
    - `helpers.py`: Helper functions used across the application.
    - `printing.py`: Functions to handle formatted printing.

### Main Entry Point

- `main.py`: The main entry point for the application.

### Navigation

- `navigation.json`: Configuration for UI navigation.


## Authors

* **Milos Petrovic** - [github](http://github.com/milosptr)
* **Tinna Maria Thorleifsdottir** 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details
