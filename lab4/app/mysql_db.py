import mysql.connector as connector 
from flask import g


# Определяем класс MySQL, определяем метод __init__
# Self переменная используется для связывания экземпляра класса к методу экземпляра
# teardown_appcontext(self.close_db) - кол бек, какая функция будет вызываться после обработки запроса
class MySQL:
    def __init__(self, app):
        self.app = app
        self.app.teardown_appcontext(self.close_db)
    
    # Вовремя обработки 1 http обработать несколько SQL запросов 
    # g - хранит в себе значения, к которым можно получить доступ
    # из любого места в программе в контексте обработки http запроса(для каждого http-свой),
    # Есть ли ключ в объекте g, если нет нужно его утстановить 
    # Если соединение установлено возвращаем его 
    # @property - позволяет образаться к методу без указания скобок
    @property
    def connection(self):
        if not 'db' in g:
            g.db = self.connect()
        return g.db

    # Соединение соединения, возвразаем объект соединения, нужно передать конфигурация для доступа к базе - получить из config.py,
    # можем обратиться к self из-за (self.app = app)
    def connect(self):
        return connector.connect(**self.config())

    def config(self):
        return {
            'user': self.app.config['MYSQL_USER'],
            'password': self.app.config['MYSQL_PASSWORD'],
            'host': self.app.config['MYSQL_HOST'],
            'database' : self.app.config['MYSQL_DATABASE'],
        }

    # Закрываем соединение
    def close_db(self, e=None):
        db = g.pop('db', None)
        if db is not None:
            db.close()