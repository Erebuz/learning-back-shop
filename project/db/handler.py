from datetime import timedelta, datetime
from hashlib import sha256

import pymysql

from project.classes.User import UserAuth


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
            user = UserAuth(user_id=row[0], login=row[1], pass_hash=row[2], roles=row[5])

        return user

    def get_user_auth(self, user_id):
        with pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                             db=self.db) as conn:
            curs = conn.cursor()
            curs.execute("SELECT user_id, login, pass_hash, group_id FROM shop.user WHERE user_id='{}'".format(user_id))
            row = curs.fetchone()
            curs.execute("SELECT name FROM shop.group WHERE group_id='{}'".format(row[3]))
            roles = curs.fetchone()
            user = UserAuth(user_id=row[0], login=row[1], pass_hash=row[2], roles=roles)

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

    def set_new_user(self, user_json, group):
        with pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                             db=self.db) as conn:
            curs = conn.cursor()

            pass_hash = sha256(bytes(user_json["password"], encoding="utf-8")).hexdigest()
            if user_json['birth_date'] == "":
                birth_date = str(datetime.today())
            else:
                birth_date = user_json['birth_date']

            sql_string = "INSERT INTO shop.user SET login='{}', pass_hash='{}', firstname='{}', lastname='{}'," \
                         "phone_number='{}', address_city='{}', address_street='{}', address_build='{}'," \
                         "address_apartment='{}', mail='{}', birth_date='{}', group_id='{}'"
            sql_string = sql_string.format(user_json['login'],
                                           pass_hash,
                                           user_json[
                                               'firstname'],
                                           user_json[
                                               'lastname'],
                                           user_json[
                                               'phone_number'],
                                           user_json['address'][
                                               'city'],
                                           user_json['address'][
                                               'street'],
                                           user_json['address'][
                                               'build'],
                                           user_json['address'][
                                               'apartment'],
                                           user_json['mail'],
                                           birth_date,
                                           group)
            curs.execute(sql_string)
            conn.commit()

    def get_user_data(self, user_id):
        with pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                             db=self.db) as conn:
            curs = conn.cursor()
            curs.execute(
                "SELECT login, firstname, lastname, phone_number, address_city, address_street, address_build, " +
                "address_apartment, mail, birth_date FROM shop.user WHERE user_id='{}'".format(
                    user_id))
            login, firstname, lastname, phone_number, address_city, address_street, address_build, address_apartment, \
            mail, birth_date = curs.fetchone()
            return {
                'mail'        : mail,
                'login'       : login,
                'firstname'   : firstname,
                'lastname'    : lastname,
                'phone_number': phone_number,
                'address'     : {
                    'city'     : address_city,
                    'street'   : address_street,
                    'build'    : address_build,
                    'apartment': address_apartment, 'mail': mail,
                },
                'birth_date'  : str(birth_date)
            }

    def edit_user_data(self, user_json, user_id):
        print(user_id)
        with pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                             db=self.db) as conn:
            pass_hash = sha256(bytes(user_json["password"], encoding="utf-8")).hexdigest()

            curs = conn.cursor()
            curs.execute(
                "UPDATE shop.user SET login='{}', pass_hash='{}', firstname='{}', lastname='{}', "
                "phone_number='{}', address_city='{}', address_street='{}', address_build='{}', "
                "address_apartment='{}', mail='{}', "
                "birth_date='{}' WHERE user_id='{}'".format(user_json['login'],
                                                            pass_hash,
                                                            user_json[
                                                                'firstname'],
                                                            user_json[
                                                                'lastname'],
                                                            user_json[
                                                                'phone_number'],
                                                            user_json['address'][
                                                                'city'],
                                                            user_json['address'][
                                                                'street'],
                                                            user_json['address'][
                                                                'build'],
                                                            user_json['address'][
                                                                'apartment'],
                                                            user_json['mail'],
                                                            user_json['birth_date'],
                                                            user_id)
            )
            conn.commit()
