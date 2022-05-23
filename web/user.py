from os import stat
from flask_login import UserMixin

USERS_DB = {}

class User(UserMixin):
    """Custom User class."""

    def __init__(self, id_, name, email):
        self.id = id_
        self.name = name
        self.email = email

    def claims(self):
        return {'name': self.name,
                'email': self.email}.items()
        
    @staticmethod
    def get(user_id):
        return USERS_DB.get(user_id)

    @staticmethod
    def create(user_id, name, email):
        USERS_DB[user_id] = User(user_id,name,email)
        