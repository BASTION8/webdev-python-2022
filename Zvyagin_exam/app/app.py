import os
from flask import Flask, render_template, request, send_from_directory, abort
from sqlalchemy import MetaData, desc
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from flask_migrate import Migrate

app = Flask(__name__)
application = app

app.config.from_pyfile('config.py')

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)

from auth import bp as auth_bp, init_login_manager
from books import bp as books_bp


app.register_blueprint(auth_bp)
app.register_blueprint(books_bp)

init_login_manager(app)

from models import *

PER_PAGE = 10


@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    books = Book.query.order_by(Book.year.desc())
    pagination = books.paginate(page, PER_PAGE)
    books = pagination.items
    book_genres = Book_genre.query.all()
    imgs = Image.query.all()
    return render_template('index.html',
                            books=books,
                            pagination=pagination, book_genres=book_genres,imgs=imgs)

@app.route('/media/images/<image_id>')
def image(image_id):
    image=Image.query.get(image_id)
    if image is None:
        abort(404)
    return send_from_directory(app.config['UPLOAD_FOLDER'], image.storage_filename)

