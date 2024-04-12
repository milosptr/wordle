from uuid import UUID, uuid4


class User:
    database = "users.json"
    file_path = f"data_layer/repository/{database}"

    def __init__(self, uuid: UUID | None, name: str, username: str):
        self.uuid = uuid if uuid is not None else uuid4()
        self.name = name
        self.username = username

    def __str__(self):
        return f"{self.name}"

    def get_id(self):
        """
        Get the user id
        """
        return self.uuid

    def get_list_of_values(self):
        """
        Get the list of values from the user
        """
        return self.__dict__.values()

    def get_json_format(self):
        """
        Get the user in JSON format
        :return: dict
        """
        return {
            'id': str(self.uuid),
            'username': str(self.username),
            'name': self.name,
        }

