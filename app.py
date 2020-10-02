from flask import Flask, render_template, session, url_for, request, jsonify
from sqlalchemy import create_engine, text
import hashlib

app = Flask(__name__)
app.config.from_pyfile('config.py')

database = create_engine(app.config['DB_URL'], encoding='utf-8')
app.database = database
print('test')
print(app.database)

SECRET_KEY = 'apple'

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

    pw_hash = hashlib.sha256(pwd.encode('utf-8')).hexdigest()

    print(email,pwd,nickname,pw_hash)

    user = request.json
    app.database.execute(text("""INSERT INTO users(email,nickname,password) VALUES(:email,nickname,pwd)"""),user).lastrowid

    return "", 200




if __name__ == '__main__':
    app.secret_key = 'Juni'
    app.run('localhost', port=9000, debug=True)