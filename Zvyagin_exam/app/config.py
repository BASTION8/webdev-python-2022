import os
SECRET_KEY = "9dd2c0eefd79ebeb5749df9f00f45e5ebc38617cfc1dcf534227ad774c1296f7"

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://std_1687_exam:bastion1488@std-mysql.ist.mospolytech.ru/std_1687_exam'
SQLALCHEMY_TRACK_MODIFICATIONS = False
ADMIN_ROLE_ID = 1
MODER_ROLE_ID = 2
USER_ROLE_ID = 3
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'images')