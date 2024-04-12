from api_layer.user_api import UserAPI
from models.User import User


class UserService:
    def __init__(self):
        self.user_dao = UserAPI()

    def get_users(self):
        return self.user_dao.get_users()

    def get_user(self, selected_user):
        return self.user_dao.get_user(selected_user)

    def add_user(self, user: User):
        self.user_dao.add_user(user)

