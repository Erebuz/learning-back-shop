from project.classes.User import User


class DBHandler:
    def __init__(self):
        users = [User(1, "admin", "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918", ['admin']),
                 User(2, "user", "04f8996da763b7a969b1028ee3007569eaf3a635486ddab211d512c85b9df8fb", ["user"])]
        self.username_table = {user.username: user for user in users}
        self.userid_table = {user.user_id: user for user in users}
        self.refresh_token_table = {}
        print("db connection set")

    def __del__(self):
        print("db connection closed")

    def get_user_by_username(self, username):
        user = self.username_table.get(username, None)
        return user

    def get_user_by_user_id(self, user_id):
        user = self.userid_table.get(user_id, None)
        return user

    def store_refresh_token(self, user_id, refresh_token):
        key = 'refresh_token_{}'.format(user_id)
        self.refresh_token_table.update({key: refresh_token})

    def get_refresh_token_by_user_id(self, user_id):
        key = f'refresh_token_{user_id}'
        token = self.refresh_token_table.get(key)
        return token
