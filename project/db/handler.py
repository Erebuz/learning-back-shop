from datetime import timedelta, date, datetime
from hashlib import sha256

import pymysql

from project.classes.User import UserAuth
from project.classes.Product import Product


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
                birth_date = str(date.today())
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

    def get_simple_user(self, user_json, group):
        with pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                             db=self.db) as conn:
            curs = conn.cursor()

            user_str = "SELECT user_id FROM user WHERE phone_number='{}'".format(user_json["phone_number"])
            curs.execute(user_str)
            user_id = curs.fetchone()

            if user_id is None:
                sql_string = "INSERT INTO shop.user SET phone_number='{}', group_id='{}'"
                sql_string = sql_string.format(user_json["phone_number"], group)
                curs.execute(sql_string)
                conn.commit()

                curs.execute(user_str)
                user_id = curs.fetchone()

            return user_id[0]

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
                'birth_date'  : str(birth_date) if birth_date is not None else ""
            }

    def edit_user_data(self, user_json, user_id):
        print(user_id)
        with pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                             db=self.db) as conn:
            curs = conn.cursor()

            birth_date = user_json['birth_date'] if user_json['birth_date'] != "" else None

            print(user_json["password"])
            if user_json["password"] != "":
                pass_hash = sha256(bytes(user_json["password"], encoding="utf-8")).hexdigest()
                print(
                    "UPDATE shop.user SET login='{}', pass_hash='{}', firstname='{}', lastname='{}', "
                    "phone_number='{}', address_city='{}', address_street='{}', address_build='{}', "
                    "address_apartment='{}', mail='{}' {} "
                    "WHERE user_id='{}';".format(user_json['login'],
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
                                                                ", birth_date='{}, '".format(birth_date) if birth_date else "",
                                                                user_id)
                )
            else:
                curs.execute(
                    "UPDATE shop.user SET login='{}', firstname='{}', lastname='{}', "
                    "phone_number='{}', address_city='{}', address_street='{}', address_build='{}', "
                    "address_apartment='{}', mail='{}' {} "
                    "WHERE user_id='{}';".format(user_json['login'],
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
                                                                ", birth_date='{}, '".format(birth_date) if birth_date else "",
                                                                user_id)
                )

            conn.commit()

    def get_product_all(self):
        with pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                             db=self.db) as conn:
            curs = conn.cursor()
            curs.execute("SELECT products_id, seller_price, product_type.name, product_type.width, "
                         "product_type.height, product_type.thickness, material, count, description, "
                         "image_path FROM shop.product, shop.product_type WHERE product.type = product_type.type_id ")

            data = curs.fetchall()
            temp = []

            for row in data:
                temp.append(Product(row).to_dict())

            return temp

    def create_new_order(self, user_id, basket):
        with pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                             db=self.db) as conn:
            curs = conn.cursor()

            for prod in basket:
                sql_str = "INSERT INTO shop.order SET product_id='{}', customer_id='{}', count='{}', status='new', date=NOW()".format(prod["id"], user_id, prod["count"])
                curs.execute(sql_str)

            conn.commit()
