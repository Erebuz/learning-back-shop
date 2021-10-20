class User:

    def __init__(self, id, username, password, scopes):
        self.user_id = id
        self.username = username
        self.password = password
        self.scopes = scopes

    def __repr__(self):
        return "User(id='{}')".format(self.user_id)

    def to_dict(self):
        return {"user_id": self.user_id, "username": self.username}
