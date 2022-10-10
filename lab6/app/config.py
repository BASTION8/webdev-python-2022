import os

SECRET_KEY = "9dd2c0eefd79ebeb5749df9f00f45e5ebc38617cfc1dcf534227ad774c1296f7"

# SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://std_1687_lab6:bastion1488@std-mysql.ist.mospolytech.ru'
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://std_1687_lab6:bastion1488@std-mysql.ist.mospolytech.ru/std_1687_lab6'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'images')
