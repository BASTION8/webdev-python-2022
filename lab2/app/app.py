from unittest import result
from urllib import response
from flask import Flask, render_template, request, make_response

# Значение request определяется текущим контекстом запроса, для каждого потока он свой, можем получить доступ к данным которые доступны в запросе
# В шаблоне доступен по умолчанию(его не нужно передавать)

app = Flask(__name__)
application = app


# К объекту запроса можем обратиться только в контексте запроса (Запрос будет когда будет вызываться функция обработчик)
@app.route('/')
def index():
    url = request.url
    return render_template('index.html')


@app.route('/args')
def args():
    return render_template('args.html')


@app.route('/headers')
def headers():
    return render_template('headers.html')



# Кроме тела ответа может передаваться служебная информация с помощью

# Чтобы сделать новое значение cookies - у ответа есть заголовки в которых мы можем что-то передать 
# Чтобы установить свой заголовок нужен объект ответа, чтобы его получить используем make_response
# make_response - Преобразуйте возвращаемое значение из функции представления в экземпляр
# И вместо render_template возвращаем make_response

# cookies - словарь
# Путь по умолчанию проставляется для всего домена, чтобы задать конкретный путь (path)
# Будет ли доступен cookie, через защищенный соединение или нет (secure)
# Доступ к cookies не доступен для скрипта, доступ только у сервера(httpoly)
# Нужно ли отправлять cookies если запрос был с другово домена(samesite)
# Для кокого поддемена будут доступны cookies (domain)
# 


@app.route('/cookies')
def cookies():
    # make_response - принимает строку с телом ответа
    response = make_response(render_template('cookies.html'))
    # set_cookie - добавляет cookie (первый агрумент название, второго значение)
    if request.cookies.get('name') is None:
        response.set_cookie('name', 'qq')
    else:
        # expires=0 - удалить запись, срок годности
        response.set_cookie('name', 'qq', expires=0)
    return response


# Добавляем методы, чтобы обрабатывать запросы, фласк по умолчанию обрабатывает GET запросы, поэтому в ручную прописываем список методов,
# которые хотим обрабатывать
# Запрос GET передает данные в URL в виде пар "имя-значение" (другими словами, через ссылку), а запрос POST передает данные в теле запроса, 
# используем в случаях, когда нужно вносить изменение, например авторизация

@app.route('/parform', methods=['GET', 'POST'])
def parform():
    return render_template('parform.html')



@app.route("/form", methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        context = {}
        num = []
        others = []
        allowed = [' ', '(', ')', '-', '.', '+']
        for i in request.form['number']:
            if i.isdigit():
                num.append(i)
            else:
                others.append(i)
        if len(num) < 10:
            context = {'error': 'номер слишком короткий'}
        elif len(others) == 3 and (len(num) == 10):
            if (others[0]=='.') and (others[1]=='.') and (others[2]=='.'):
                number = '8-' + str(num[0]) + str(num[1]) + str(num[2]) + '-' + str(num[3]) + str(num[4]) + str(num[5]) +'-' + str(num[6]) + str(num[7]) + '-' + str(num[8]) + str(num[9])
                print('верный формат')
            else:
                context = {'error': 'номер содержит недопустимые символы'}
        elif (int(num[0]) == 8 or (int(num[0])==7 and others[0]=='+')) and len(num) == 11:
            number = '8-' + str(num[1]) + str(num[2]) + str(num[3]) + '-' + str(num[4]) + str(num[5]) + str(num[6]) +'-' + str(num[7]) + str(num[8]) + '-' + str(num[9]) + str(num[10])
            print('верный формат')
        else:
            context = {'error': 'номер слишком длинный'}
        # Проверка каждого спецсимвола которые у нас попал в others, на соответсвие допустимых спецсимволов
        # Если хоть один спец символ не соответствует => ошибка
        for symbol in others:
            if symbol not in allowed:
                context = {'error': 'номер содержит недопустимые символы'}
        if context:
            return render_template('form.html', context=context )
        else:
            return render_template('form.html', number=number)
    return render_template('form.html')


  