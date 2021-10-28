from datetime import timedelta, datetime

import pymysql

from project.classes.User import User


class DBHandler:
    def __init__(self):
        self.host = 'localhost'
        self.port = 3306
        self.user = "root"
        self.passwd = '1234'
        self.db = 'shop'

    def get_user_by_username(self, username):
        with pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                             db=self.db) as conn:
            curs = conn.cursor()
            curs.execute("SELECT * FROM user WHERE login='{}'".format(username))
            row = curs.fetchone()
            user = User(user_id=row[0], login=row[1], pass_hash=row[2], roles=row[5])

        return user

    def get_user_by_user_id(self, user_id):
        with pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                             db=self.db) as conn:
            curs = conn.cursor()
            curs.execute("SELECT user_id, login, pass_hash, group_id FROM shop.user WHERE user_id='{}'".format(user_id))
            row = curs.fetchone()
            curs.execute("SELECT name FROM shop.group WHERE group_id='{}'".format(row[3]))
            roles = curs.fetchone()
            user = User(user_id=row[0], login=row[1], pass_hash=row[2], roles=roles)

        return user

    def store_refresh_token(self, user_id, refresh_token):
        with pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                             db=self.db) as conn:
            curs = conn.cursor()
            curs.execute(
                "UPDATE user SET refresh_token = '{}', token_date = NOW() WHERE user_id={}".format(refresh_token,
                                                                                                   user_id))
            conn.commit()

    def get_refresh_token_by_user_id(self, user_id):
        with pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                             db=self.db) as conn:
            curs = conn.cursor()
            curs.execute("SELECT refresh_token, token_date FROM shop.user WHERE user_id='{}'".format(user_id))
            token, date = curs.fetchone()

            shift = timedelta(hours=480)
            if (date + shift) < datetime.today():
                return None

            return token
