from flask import Flask, render_template
from faker import Faker

fake = Faker()

app = Flask(__name__)
application = app

images_ids = [
    '2d2ab7df-cdbc-48a8-a936-35bba702def5'
    '6e12f3de-d5fd-4ebb-855b-8cbc485278b7'
    '7d4e9175-95ea-4c5f-8be5-92a6b708bb3c'
    'afc2cfe7-5cac-4b80-9b9a-d5c65ef0c728'
    'cab5b7f2-774e-4884-a200-0c0180fa777f'
]

def generate_post(index):
    return {
        'title': 'Заголовок поста',
        'author': fake.name(),
        'text': fake.paragraph(nb_sentences=100),
        'date': fake.date_time_between(start_date='-2y', end_date='now'),
        'image_filename': f'{images_ids[index]}.jpg'
    }

posts_list = sorted([generate_post(i) for i in range(5)], key=lambda x: x['date'], reverse=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts')
def posts():
    title = "Посты"
    return render_template('posts.html', posts=posts_list)

@app.route('/posts/<int:index>') 
def post(index):
    p = posts_list[index]
    return render_template('post.html', post=p, title=p['title'])

@app.route('/about')
def about():
    title = "Об авторе"
    return render_template('about.html', title=title)