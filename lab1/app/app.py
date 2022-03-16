from email.mime import application
from flask import Flask, render_template

app = Flask(__name__)
application = app

@app.route('/')
def index():
    msg = "Hello"
    return render_template('index.html', message=msg)