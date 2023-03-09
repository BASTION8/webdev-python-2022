from flask import Blueprint, render_template, redirect, url_for, flash, request
from models import *
from flask_login import current_user, login_required
from auth import *
import bleach
from tools import ImageSaver
import markdown


bp = Blueprint('books', __name__, url_prefix='/books')

BOOKS_PARAMS = ['name', 'short_description', 'year', 'publishing_house', 'author', 'page_volume']

REVIEWS_PARAMS = ['book_id', 'user_id', 'rating', 'text']


def params():
    return { p: request.form.get(p) for p in BOOKS_PARAMS }


def review_params():
    return {p: request.form.get(p) for p in REVIEWS_PARAMS}


@bp.route('/new')
@check_rights('create')
@login_required
def new():
    genres = Genre.query.all()
    return render_template('books/new.html', genres=genres)



@bp.route('/new', methods=['POST'])
@check_rights('create')
@login_required
def create():
    book = Book(**params())
    # Cанитайзер чтобы экранировать все потенциально опасные теги
    book.short_description = bleach.clean(book.short_description)
    
    try:
        db.session.add(book)
        db.session.commit()
    except: 
        db.session.rollback()
        flash('Введены некорректные данные или не все поля заполнены. Ошибка сохранения', 'danger')
        return redirect(url_for('books.new'))

    genres = request.form.getlist('genres')
    for genre in genres:
        book_genre = Book_genre(book_id=book.id, genre_id=genre)
        db.session.add(book_genre)
        db.session.commit()
    
    try:
        f = request.files.get('background_img')
        if f and f.filename:
            img_saver = ImageSaver(f)
            img = img_saver.save()
        img_saver.bind_to_object(book)
    except:
        db.session.delete(book)
        db.session.commit()
        flash('У книги нет обложки. Ошибка сохранения', 'danger')
        return redirect(url_for('books.new'))

    flash(f'Книга "{book.name}" была успешно добавлена!', 'success')

    return redirect(url_for('index'))



@bp.route('/edit/<int:book_id>')
@check_rights('edit')
@login_required
def edit(book_id):
    book = Book.query.get(book_id)
    genres = Genre.query.all()
    book_genres  = Book_genre.query.all()
    return render_template('books/edit.html', genres=genres, book=book, book_genres=book_genres)


@bp.route('/edit/<int:book_id>', methods=['POST'])
@check_rights('edit')
@login_required
def update(book_id):
    book = Book.query.get(book_id)
    edit_params = params()
    book.name = edit_params['name']
    # Cанитайзер чтобы экранировать все потенциально опасные теги
    book.short_description = bleach.clean(book.short_description)
    book.short_description = edit_params['short_description']
    book.year = edit_params['year']
    book.author = edit_params['author']
    book.page_volume = edit_params['page_volume']
    
    genres_old = Book_genre.query.filter_by(book_id=book_id).all()
    for genres in genres_old:
        db.session.delete(genres)

    genres = request.form.getlist('genres')
    for genre in genres:
        book_genre = Book_genre(book_id=book.id, genre_id=genre)
        db.session.add(book_genre)
    
    db.session.commit()
    flash(f'Книга "{book.name}" была успешно обновлена.', 'success')
    return redirect(url_for('index'))


@bp.route('/show/<int:book_id>')
def show(book_id):
    book = Book.query.get(book_id)
    book.short_desc = markdown.markdown(book.short_description)
    book_genres = Book_genre.query.all()
    reviews = Reviews.query.filter(Reviews.book_id == book_id)
    check_user = False
    if current_user.is_authenticated:
        for review in reviews:
            if review.user_id == current_user.id:
                check_user = True
   
    imgs = Image.query.all()
    
    return render_template('books/show.html',book=book,book_genres=book_genres, reviews=reviews, imgs=imgs, check_user=check_user)

@bp.route('/delete/<int:book_id>', methods=['POST'])
@login_required
@check_rights('delete')
def delete(book_id):
    book = Book.query.filter_by(id=book_id).first()
    book_name = book.name
    img = Image.query.filter_by(book_id=book_id).first()
    img_path = os.path.join(os.path.dirname(os.path.abspath(
        __file__)), 'media', 'images') + '\\' + img.storage_filename
    db.session.delete(book)
    db.session.commit()
    os.remove(img_path)
    flash(f'Книга {book_name} была успешно удалена!', 'success')
    return redirect(url_for('index'))



@bp.route('/review/<int:book_id>')
@login_required
def review(book_id):
    book = Book.query.get(book_id)
    return render_template('books/review.html', book=book)

@bp.route('/review/<int:book_id>', methods=['POST'])
@login_required
def addreview(book_id):
    review = Reviews(**review_params())
    # Cанитайзер чтобы экранировать все потенциально опасные теги
    review.text = bleach.clean(review.text)
    book = Book.query.filter_by(id=book_id).first()
    book.grade_amount += 1
    book.grade_sum += int(review.rating)

    try:
        db.session.add(review)
        db.session.commit()
    except:
        db.session.rollback()
        flash('Рецензия не была добавлена!', 'danger')
        return redirect(url_for('books.show', book_id=book_id))

    flash('Рецензия была успешно добавлена!', 'success')
    return redirect(url_for('books.show', book_id=book_id))