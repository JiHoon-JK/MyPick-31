from datetime import timedelta

from flask import Flask, render_template, session, url_for, request, jsonify, app
from pymongo import MongoClient
import hashlib

client = MongoClient('mongodb://bibi:6666667!@3.34.129.197', 27017)
db = client.MyPick31

app = Flask(__name__)

SECRET_KEY = 'apple'

############
#라우팅 함수# : 홈 / 디테일 / 회원가입 / 로그인 / about MyPick31 / DB페이지
############
@app.route('/')
def home_page():
    para = request.args.get("base")
    print(para)
    # 로그인하고 조회(세션 값안에 auth_id 가 있다면, 로그인을 진행했다면 세션이 형성되어있어서 체크 가능)
    if 'auth_id' in session:
        session_id = session['auth_id']
        print('Logged in as '+session_id)
        print(session)
        session_nickname = session['nickname']
        print(session_nickname)
        return render_template('index.html', session_id=session_id, session_nickname=session_nickname, para_data=para)
    # 로그인 없이 조회
    else:
        return render_template('index.html', para_data=para)

@app.route('/detail')
def detail_page():
    # 로그인하고 조회(세션 값안에 auth_id 가 있다면, 로그인을 진행했다면 세션이 형성되어있어서 체크 가능)
    if 'auth_id' in session:
        session_id = session['auth_id']
        print('Logged in as ' + session_id)
        print(session)
        session_nickname = session['nickname']
        print(session_nickname)
        return render_template('detail.html', session_id=session_id, session_nickname=session_nickname)
    # 로그인 없이 조회
    else:
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

# db에 데이터 넣는 html
@app.route('/insert_db')
def insert_db_page():
    return render_template('db_insert.html')


########################
#회원가입, 로그인, 로그아웃#
########################

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

    userdb = list(db.userdb.find({}))

    for i in range(len(userdb)):
        print(userdb[i])
        if userdb[i].get('auth_id') == receive_id:
            if userdb[i].get('pwd') == pwd_hash:
                user_nickname = userdb[i].get('nickname')
                print(user_nickname)
                # session 형성
                session['auth_id'] = receive_id
                session['nickname'] = user_nickname
                session.permanent = True
                # session 유지 시간은 5분으로 한다.
                app.permanent_session_lifetime = timedelta(minutes=5)

                return jsonify({'result':'success','userdb':user_nickname})
            else:
                return jsonify({'result':'fail1','userdb':'failed'})
    else:
        return jsonify({'result':'fail2','userdb':'failed'})

#로그아웃
@app.route('/customer_logout', methods=['POST'])
def logout():
    session.pop('email',None)
    return jsonify({'result':'success'})

###############
#DB insert API#
###############
# Category-Base
@app.route('/createCB', methods=['POST'])
def createCB():
    cbase1 = request.form['cbase1']
    cbase2 = request.form['cbase2']
    doc = {
        'cbase1': cbase1,
        'cbase2': cbase2
    }
    db.cbase.insert_one(doc)
    return jsonify(({'result':'success','msg':'cbase에 저장완료'}))

# Category-Topping
@app.route('/createCT', methods=['POST'])
def createCT():
    ctopping1 = request.form['ctopping1']
    ctopping2 = request.form['ctopping2']
    doc = {
        'ctopping1': ctopping1,
        'ctopping2': ctopping2
    }
    db.ctopping.insert_one(doc)
    return jsonify(({'result':'success','msg':'ctopping에 저장완료'}))

# Category - Syrup
@app.route('/createCS', methods=['POST'])
def createCS():
    csyrup1 = request.form['csyrup1']
    csyrup2 = request.form['csyrup2']
    doc = {
        'csyrup1': csyrup1,
        'csyrup2': csyrup2
    }
    db.csyrup.insert_one(doc)
    return jsonify(({'result':'success','msg':'csyrup에 저장완료'}))


# Flavor - Signature
@app.route('/createF_SG', methods=['POST'])
def createF_signature():
    id = request.form['id']
    print(id);
    name = request.form['name']
    name_eng = request.form['name_eng']
    base = request.form['base']
    topping = request.form['topping']
    syrup = request.form['syrup']
    kcal = request.form['kcal']
    allergens = request.form['allergens']
    img = request.form['img']
    doc = {
        'id': id,
        'name': name,
        'name_eng': name_eng,
        'base': base,
        'topping': topping,
        'syrup': syrup,
        'kcal': kcal,
        'allergens': allergens,
        'img': img
    }
    db.signature.insert_one(doc)
    return(jsonify({'result':'success','msg':'signature 저장완료'}))

# db_insert
@app.route('/createF_SS', methods=['POST'])
def createF_season():
    id = request.form['id']
    name = request.form['name']
    name_eng = request.form['name_eng']
    base = request.form['base']
    topping = request.form['topping']
    syrup = request.form['syrup']
    kcal = request.form['kcal']
    allergens = request.form['allergens']
    img = request.form['img']
    doc = {
        'id': id,
        'name': name,
        'name_eng': name_eng,
        'base': base,
        'topping': topping,
        'syrup': syrup,
        'kcal': kcal,
        'allergens': allergens,
        'img': img
    }
    db.season.insert_one(doc)
    return(jsonify({'result':'success','msg':'season 저장완료'}))


###############
#DB insert API#
###############
# bring_db
@app.route('/bring_ice_cream', methods=['GET'])
def bring_ice_cream():
    ice_cream = request.args.get('ice_cream')
    print("==================")
    print(ice_cream)
    bring_signature_db = list(db.signature.find({'base':ice_cream},{'_id':0}))
    bring_season_db = list(db.season.find({'base':ice_cream},{'_id':0}))
    print(bring_signature_db)
    print(bring_season_db)
    total_data = bring_signature_db + bring_season_db
    print(total_data)
    return(jsonify({'result':'success','data':total_data}))


# Flavor - Season

#################
#Review Save API#
#################
@app.route('/save_review', methods=['POST'])
def save_reivew():
    ice_cream_name = request.form['ice_cream_name']
    reviewer = request.form['reviewer']
    review = request.form['review']

    doc = {
        'ice_cream': ice_cream_name,
        'reviewer': reviewer,
        'review': review
    }

    db.review.insert_one(doc)
    return(jsonify({'result':'success', 'msg':'review 저장완료'}))

if __name__ == '__main__':
    app.secret_key = 'Juni'
    app.run('localhost', port=9000, debug=True)