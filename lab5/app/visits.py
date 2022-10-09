import math
import io
import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from app import mysql
from auth import init_login_manager, bp as auth_bp, chech_rights


bp = Blueprint('visits', __name__, url_prefix='/visits')


# Количество записей на странице
PER_PAGE = 5

def convert_to_csv(records):
    # Извелкаем поля из результатов запроса
    # берем запись и берем атрибут 
    # _ - служебный атрибут 
    fields = records[0]._fields
    # Порядковый номер + значение полей через ,
    result = 'NO,' + ','.join(fields) +'\n'
    # для каждой записи списка сформировать строку в csv файлик
    #  возвращает итератор, который при очередном вызове возвращает пару index и сам элемент  
    for i, record in enumerate(records):
        # 
        result += f'{i+1},' + ','.join([str(getattr(record, f, '')) for f in fields]) +'\n'
    return result

# функция генерация BytesIO и записи данных (можем работать как с файлом )
def generate_report(records):
    buffer = io.BytesIO() 
    #Вернет строку а encode - вернет двоичное представление строки
    buffer.write(convert_to_csv(records).encode('utf-8'))
    # Возвращает указать в самое начало тк 0
    buffer.seek(0)
    return buffer


# Журнал посещёний, отображаем записи страницы visit_logs
@bp.route('/logs')
def logs():
    # Текущая страница
    page = request.args.get('page', 1, type=int)
    # Запрос на количество записей
    with mysql.connection.cursor(named_tuple=True) as cursor:
        cursor.execute('SELECT COUNT(*) AS count FROM visit_logs;')
        total_count  = cursor.fetchone().count
    # Округлить в большую сторону 
    total_pages = math.ceil(total_count/PER_PAGE)
    # Запрос к базе
    with mysql.connection.cursor(named_tuple=True) as cursor:
        # Отображаем пользователя, путь до станицы, и дата действия
        # JOIN users ON visit_logs.user_id = users.id объединяет 2 талицы по users.id
        # LEFT JOIN - чтобы были записы таблицы visit_logs, но у которых users.id пустое и нет пары в таблице user
        # ORDER BY created_at DESC (по убыванию) - сотрировка, чтобы показывать последнее действие
        cursor.execute(('SELECT visit_logs.*, users.last_name, users.first_name, users.middle_name FROM visit_logs LEFT JOIN users ON visit_logs.user_id = users.id ORDER BY visit_logs.created_at DESC '
                        'LIMIT %s OFFSET %s;'), (PER_PAGE, PER_PAGE*(page-1)))
        records = cursor.fetchall()
    # возвращает шаблон, и передаем записи которые есть в табличке
    return render_template('visits/logs.html', records=records, page=page, total_pages=total_pages)

# Статистика по пользователям
@bp.route('/stats/users')
@chech_rights('assign_role')
def users_stat():
    # COUNT (*) - посчитает количество строк не равных 0
    # GROUP BY - берем уникальные значения(visit_logs.user_id), записи с одинаковым значением образуют группы
    # и по этим группам мы вычисляем функции которые мы указываем(COUNT (*))
    # Сортировка в порядке убывания - ORDER BY count DESC
    # AS count - даем название чтобы можно было обратиться 
    query = ('SELECT users.last_name, users.first_name, users.middle_name, COUNT(*) AS count '
            'FROM users RIGHT JOIN visit_logs ON visit_logs.user_id = users.id '
            'GROUP BY visit_logs.user_id '
            'ORDER BY count DESC;')
    with mysql.connection.cursor(named_tuple=True) as cursor:
        cursor.execute(query)
        records = cursor.fetchall()

    if request.args.get('download_csv'):
        f = generate_report(records)
        filename = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S') + '_users_stat.csv'
        # mimetype - если не укажем то автоматически будет определять расширение
        # as_attachment - позволяет указать будет ли браузер предлагать скачать(куда сохранить), или попытается открыть сам(True - скачивался)
        # attachment_filename - имя файла 
        return send_file(f, mimetype='text/csv', as_attachment=True, attachment_filename=filename)

    return render_template('visits/users_stat.html', records=records)


@bp.route('/stats/pages')
@chech_rights('assign_role')
def pages_stat():
    query = ('SELECT visit_logs.path, COUNT(*) AS count FROM visit_logs GROUP BY visit_logs.path ORDER BY count DESC; ')
    with mysql.connection.cursor(named_tuple=True) as cursor:
        cursor.execute(query)
        records = cursor.fetchall()

    if request.args.get('download_csv'):
        f = generate_report(records)
        filename = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S') + '_users_stat.csv'
        # mimetype - если не укажем то автоматически будет определять расширение
        # as_attachment - позволяет указать будет ли браузер предлагать скачать(куда сохранить), или попытается открыть сам(True - скачивался)
        # attachment_filename - имя файла 
        return send_file(f, mimetype='text/csv', as_attachment=True, attachment_filename=filename)

    return render_template('visits/pages_stat.html', records=records)