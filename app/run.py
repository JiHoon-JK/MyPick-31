from datetime import datetime

from flask import Flask, render_template, session, url_for, request, jsonify
from pymongo import MongoClient
import hashlib

client = MongoClient('localhost', 27017)
db = client.MyPick31

app = Flask(__name__)

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
@app.route('/customer_register', methods=['POST'])
def register():
    auth_id = request.form['auth_id']
    pwd = request.form['pwd']
    nickname = request.form['nickname']

    # 패스워드 암호화
    pw_hash = hashlib.sha256(pwd.encode('utf-8')).hexdigest()

    userdb = list(db.userdb.find({}))

    # userdb 를 새로 만드는 경우
    if len(userdb) == 0:
        db.userdb.insert_one({'auth_id':auth_id,'pwd':pw_hash,'nickname':nickname})
        return jsonify({'result':'success'})

    else:
        for i in range(len(userdb)):
            if userdb[i].get('auth_id') == auth_id:
                return jsonify({'result': 'fail1'})
            elif userdb[i].get('nickname') == nickname:
                return jsonify({'result':'fail2'})

        db.userdb.insert_one({'auth_id':auth_id,'pwd':pw_hash,'nickname':nickname})
        return jsonify({'result':'success','userdb':auth_id})


# 로그인
@app.route('/customer_login', methods=['POST'])
def login():

    receive_id = request.form['receive_id']
    receive_pwd = request.form['receive_pwd']
    pwd_hash = hashlib.sha256(receive_pwd.encode('utf-8')).hexdigest()

    print(receive_id)

    # session 형성
    session['auth_id'] = receive_id
    session.permanent = True

    userdb = list(db.userdb.find({}))

    for i in range(len(userdb)):
        print(userdb[i])
        if userdb[i].get('auth_id') == receive_id:
            if userdb[i].get('pwd') == pwd_hash:
                user_nickname = userdb[i].get('nickname')
                print(user_nickname)
                return jsonify({'result':'success','userdb':user_nickname})
            else:
                return jsonify({'result':'fail1','userdb':'failed'})
    else:
        return jsonify({'result':'fail2','userdb':'failed'})

#로그아웃
app.route('/customer_logout', method=['POST'])
def logout():
    session.pop('email',None)
    return jsonify({'result':'success'})


if __name__ == '__main__':
    app.secret_key = 'Juni'
    app.run('localhost', port=9000, debug=True)