import json
from pathlib import Path

from models.User import User


class UserAPI:
    def __init__(self):
        self.user_file_path = Path(User.file_path)
        # Ensure the user file exists
        self.user_file_path.touch(exist_ok=True)

    def get_users(self):
        """Retrieves all users."""
        try:
            with self.user_file_path.open('r', encoding='utf-8') as file:
                users = json.load(file)
        except json.JSONDecodeError:
            return None

        return [User(user['id'], user['username'], user['name']) for user in users]

    def get_user(self, selected_user):
        """Retrieves a user by ID."""
        try:
            with self.user_file_path.open('r', encoding='utf-8') as file:
                users = json.load(file)
        except json.JSONDecodeError:
            return None

        for user in users:
            if user['username'] == selected_user or str(user['id']) == str(selected_user):
                return User(user['id'], user['name'], user['username'])

        return None

    def add_user(self, user: User):
        """Adds a new user to the user file."""
        with self.user_file_path.open('r+', encoding='utf-8') as file:
            try:
                users = json.load(file)
            except json.JSONDecodeError:
                users = []

            # Check if the user already exists
            for existing_user in users:
                if existing_user['username'] == user.username:
                    raise ValueError(f"User with username {user.username} already exists.")

            # Append the new user
            users.append(user.get_json_format())

            # Move back to the start of the file to overwrite it
            file.seek(0)
            json.dump(users, file, indent=4)
            file.truncate()
