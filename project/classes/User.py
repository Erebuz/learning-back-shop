class User:

    def __init__(self, user_id, login, pass_hash, roles):
        self.user_id = user_id
        self.username = login
        self.pass_hash = pass_hash
        self.roles = roles

    def __repr__(self):
        return "User(id='{}')".format(self.user_id)

    def to_dict(self):
        return {"user_id": self.user_id, "username": self.username, "roles": self.roles}
