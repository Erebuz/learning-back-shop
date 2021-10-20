from project.classes.User import User


class DBHandler:
    def __init__(self):
        users = [User(1, "admin", "admin", ['admin']), User(2, "user", "user", ["user"])]
        self.username_table = {user.username: user for user in users}
        self.userid_table = {user.user_id: user for user in users}
        print("db connection set")

    def __del__(self):
        print("db connection closed")

    def get_user_by_username(self, username):
        user = self.username_table.get(username, None)
        return user

    def get_user_by_user_id(self, user_id):
        user = self.userid_table.get(user_id, None)
        return user
