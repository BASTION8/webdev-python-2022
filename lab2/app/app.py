from urllib import response
from flask import Flask, render_template, request, make_response

app = Flask(__name__)
application = app


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form')
def form():
    return render_template('form.html')    

@app.route('/args')
def args():
    return render_template('args.html')

@app.route('/headers')
def headers():
    return render_template('headers.html')

@app.route('/cookies')
def cookies():
    response = make_response(render_template('cookies.html'))
    if request.cookies.get('name') is None:
        response.set_cookie('name', 'qq')
    else:
        response.set_cookie('name', 'qq', expires=0)
    return response