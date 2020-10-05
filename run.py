from datetime import datetime

from flask import Flask, render_template, session, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_pyfile('config.py')

SECRET_KEY = 'apple'

app.config['SECRET_KEY'] = 'this is secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __table_name__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    nickname = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self,username,nickname,password, **kwargs):
        self.username = username
        self.nickname = nickname

        self.set_password(password)

    def __repr__(self):
        return f"<User('{self.id}', '{self.username}', '{self.nickname}'"

    def set_password(self,password):
        self.password = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password, password)

class Like(db.Model):
    __table_name__ = 'like_icecream'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    ice_cream = db.Column(db.String())
    date_posted = db.Column(db.DateTime, default=datetime.utcnow())

    user_id = db.Column(db.Integer, db.ForeignKey('user_id'))

    def __repr__(self):
        return f"<Like('{self.id}', '{self.ice_cream}')>"

# 라우팅 함수
@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/detail')
def detail_page():
    return render_template('detail.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

# 회원가입
@app.route('/customer', methods=['POST'])
def register():
    email = request.form['email']
    pwd = request.form['pwd']
    nickname = request.form['nickname']

    # 패스워드 암호화
    pw_hash = hashlib.sha256(pwd.encode('utf-8')).hexdigest()

    print(email,pwd,nickname,pw_hash)

    user = request.json

    return "", 200




if __name__ == '__main__':
    app.secret_key = 'Juni'
    app.run('localhost', port=9000, debug=True)