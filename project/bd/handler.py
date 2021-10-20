from project.classes.User import User


users = [User(1, "admin", "admin", ['admin']), User(2, "user", "user", ["user"])]

username_table = {user.username: user for user in users}
userid_table = {user.user_id: user for user in users}
