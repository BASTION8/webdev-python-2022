from importlib.metadata import metadata
from flask import Flask, render_template
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
application = app

app.config.from_pyfile('config.py')

from auth import bp as auth_bp, init_login_manager
app.register_blueprint(auth_bp)

init_login_manager(app)

metadata = MetaData(app, metadata=metadata)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    categories = []
    return render_template(
        'index.html', 
        categories=categories,
    )
