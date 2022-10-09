from unicodedata import category
from flask import Blueprint, flash, redirect, render_template, request, request_finished, url_for
from app import db
from models import *
from tools import CoursesFilter, ImageSaver
from flask_login import current_user, login_required

bp = Blueprint('courses', __name__, url_prefix='/courses')

PER_PAGE = 3

COMMENT_PAGE = 5

COURSE_PARAMS = ['author_id', 'name', 'category_id', 'short_desc', 'full_desc']

REVIEW_PARAMS = ['rating', 'text', 'course_id', 'user_id']


def params():
    return { p: request.form.get(p) for p in COURSE_PARAMS }

def reviews_params():
    return { p: request.form.get(p) for p in REVIEW_PARAMS }

def search_params():
    return {
        'name': request.args.get('name'),
        'category_ids': request.args.getlist('category_ids'),
    }

@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    courses = CoursesFilter(**search_params()).perform()
    pagination = courses.paginate(page, PER_PAGE)
    courses = pagination.items 
    categories = Category.query.all()
    return render_template('courses/index.html',
                            courses=courses,
                            categories=categories,
                            pagination=pagination,
                            search_params=search_params())

@bp.route('/new')
def new():
    categories = Category.query.all()
    users = User.query.all()
    return render_template('courses/new.html',
                            categories=categories,
                            users=users)

@bp.route('/create', methods=['POST'])
def create():

    f = request.files.get('background_img')
    if f and f.filename:
        img = ImageSaver(f).save()

    course = Course(**params(), background_image_id=img.id)
    db.session.add(course)
    db.session.commit()

    flash(f'Курс {course.name} был успешно добавлен!', 'success' )

    return redirect(url_for('courses.index'))

@bp.route('/<int:course_id>')
def show(course_id):
    courses = Course.query.get(course_id)
    reviews = Review.query.filter_by(course_id=course_id).limit(COMMENT_PAGE)
    user_review = None
    if current_user.is_authenticated is True:
        user_review = Review.query.filter_by(course_id=course_id, user_id=current_user.id).first()
    users = User.query.all()

    return render_template('courses/show.html', course=courses, review=reviews, users=users, user_review=user_review)


@login_required
@bp.route('/<int:course_id>', methods=['POST'])
def create_reviews(course_id):
    reviews = Review(**reviews_params())
    courses = Course.query.filter_by(id=course_id).first()
    courses.rating_num += 1
    courses.rating_sum += int(reviews.rating)
    db.session.add(reviews)
    db.session.commit()
    flash('Комментарий был успешно добавлен!', 'success')
    return redirect(url_for('courses.show', course_id=courses.id))
