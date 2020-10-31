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
## + 홈페이지 : 아이스크림 필터링함수 포함..
@app.route('/')
def home_page():
    # 로그인하고 조회(세션 값안에 email 이 있다면, 로그인을 진행했다면 세션이 형성되어있어서 체크 가능)
    if 'email' in session:
        email1 = session['email']
        print('Logged in as '+email1)
        a = list(db.userdb.find({'auth_id': email1}, {'_id': 0}))
        print(a[0].get('nickname'))
        return render_template('index.html', session_email=email1, session_nickname=a[0].get('nickname'))
    # 로그인 없이 조회
    else:
        return render_template('index.html')

@app.route('/detail')
def detail_page():
    # URL로 보낸 아이스크림 가져오기
    ice_cream = request.args.get("ice_cream")
    # 로그인하고 조회(세션 값안에 auth_id 가 있다면, 로그인을 진행했다면 세션이 형성되어있어서 체크 가능)
    if 'email' in session:
        email1 = session['email']
        print('Logged in as '+email1)
        a = list(db.userdb.find({'auth_id': email1}, {'_id': 0}))
        print(a[0].get('nickname'))
        return render_template('detail.html', session_email=email1, session_nickname=a[0].get('nickname'), para_data=ice_cream)
    # 로그인 없이 조회
    else:
        return render_template('detail.html', para_data=ice_cream)

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/about')
def about_page():
    # 로그인하고 조회(세션 값안에 auth_id 가 있다면, 로그인을 진행했다면 세션이 형성되어있어서 체크 가능)
    if 'email' in session:
        email1 = session['email']
        print('Logged in as ' + email1)
        a = list(db.userdb.find({'auth_id': email1}, {'_id': 0}))
        print(a[0].get('nickname'))
        return render_template('about.html', session_email=email1, session_nickname=a[0].get('nickname'))
    # 로그인 없이 조회
    else:
        return render_template('about.html')


# db에 데이터 넣는 html
@app.route('/insert_db')
def insert_db_page():
    # 로그인하고 조회(세션 값안에 auth_id 가 있다면, 로그인을 진행했다면 세션이 형성되어있어서 체크 가능)
    if 'email' in session:
        email1 = session['email']
        print('Logged in as ' + email1)
        a = list(db.userdb.find({'auth_id': email1}, {'_id': 0}))
        print(a[0].get('nickname'))
        return render_template('db_insert.html', session_email=email1, session_nickname=a[0].get('nickname'))
    # 로그인 없이 조회
    else:
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

    session['email'] = receive_id
    session.permanent = True
    # session 유지 시간은 5분으로 한다.
    app.permanent_session_lifetime = timedelta(minutes=10)

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
@app.route('/customer_logout', methods=['POST'])
def logout():
    session.pop('email',None)
    return jsonify({'result':'success'})

########################
#아이스크림 정보 가져오기# -> detail에서 사용
########################
@app.route('/bring_ice_cream', methods=['GET'])
def bring_all_ice_cream():
    ice_cream = request.args.get('ice_cream')
    bring_signature_db = list(db.signature.find({'name':ice_cream},{'_id':0}))
    bring_season_db = list(db.season.find({'name':ice_cream},{'_id':0}))
    return(jsonify({'result':'success', 'signature_data':bring_signature_db, 'season_data':bring_season_db}))

##################
##아이스크림 필터링##
##################

# bring_signature_db
@app.route('/bring_signature_ice_cream', methods=['GET'])
def bring_signature_ice_cream():
    ice_cream = request.args.get('ice_cream')
    # 모든 아이스크림을 가져올 때
    if ice_cream == None:
        bring_signature_db = list(db.signature.find({},{'_id':0}))
        return(jsonify({'result':'success_1','data':bring_signature_db}))
    #필터링으로 아이스크림을 가져올 때
    else:
        bring_signature_db = list(db.signature.find({'base':ice_cream},{'_id':0}))
        return(jsonify({'result':'success_2','data':bring_signature_db}))

# bring_season_db
@app.route('/bring_season_ice_cream', methods=['GET'])
def bring_season_ice_cream():
    ice_cream = request.args.get('ice_cream')
    # 모든 아이스크림을 가져올 때
    if ice_cream == None:
        bring_season_db = list(db.season.find({},{'_id':0}))
        return(jsonify({'result':'success_1','data':bring_season_db}))
    #필터링으로 아이스크림을 가져올 때
    else:
        bring_season_db = list(db.season.find({'base':ice_cream},{'_id':0}))
        return(jsonify({'result':'success_2','data':bring_season_db}))




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

# Flavor - Season
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

############
# Like API #
############
@app.route('/like_ice_cream', methods=['POST'])
def like_ice_cream():
    ice_cream = request.form['ice_cream_name']
    like_user_nickname = request.form['like_user_nickname']
    like_db_check = list(db.like.find({'ice_cream':ice_cream,'user_nickname':like_user_nickname},{'_id':0}))
    print(like_db_check)
    if len(like_db_check) == 0:
        doc = {
            'ice_cream': ice_cream,
            'user_nickname': like_user_nickname
        }
        db.like.insert_one(doc)
        return jsonify({'result': 'success_1','msg':'likeDB에 추가'})
    else:
        return jsonify({'result': 'success_2', 'msg':'likeDB에 있습니다.'})

@app.route('/check_like_ice_cream', methods=['POST'])
def check_like_ice_cream():
    ice_cream = request.form['ice_cream_name']
    like_user_nickname = request.form['like_user_nickname']
    like_db_check = list(db.like.find({'ice_cream':ice_cream,'user_nickname':like_user_nickname},{'_id':0}))
    if len(like_db_check) == 1:
        return jsonify({'result': 'success', 'msg':'yes_check'})
    if len(like_db_check) == 0:
        return jsonify({'result': 'success', 'msg':'no_check'})

@app.route('/like_cancel_ice_cream', methods=['POST'])
def cancel_like_ice_cream():
    ice_cream = request.form['ice_cream_name']
    like_user_nickname = request.form['like_user_nickname']
    db.like.remove({'ice_cream':ice_cream,'user_nickname':like_user_nickname})
    return jsonify({'result': 'success'})

@app.route('/counting_like' , methods=['POST'])
def counting_like():
    ice_cream = request.form['ice_cream_name']
    like_db_check = list(db.like.find({'ice_cream': ice_cream}, {'_id': 0}))
    print(like_db_check)
    print(len(like_db_check))
    return jsonify({'result': 'success', 'like_count':len(like_db_check)})

############
#Review API#
############

# Review Edit
@app.route('/edit_review', methods=['POST'])
def edit_review():
    ice_cream_name = request.form['ice_cream_name']
    reviewer = request.form['reviewer']
    edit_review = request.form['edit_review']
    update_review_db = list(db.review.update({'reviewer': reviewer, 'ice_cream': ice_cream_name},{'$set': {'review': edit_review}}))
    return jsonify({'result': 'success', 'data':update_review_db})

# Review Save
@app.route('/save_review', methods=['POST'])
def save_reivew():
    ice_cream_name = request.form['ice_cream_name']
    reviewer = request.form['reviewer']
    review = request.form['review']

    check_reviewer = list(db.review.find({'ice_cream':ice_cream_name,'reviewer':reviewer},{'_id':0}))
    print(check_reviewer)
    if len(check_reviewer) == 0:
        doc = {
            'ice_cream': ice_cream_name,
            'reviewer': reviewer,
            'review': review
        }
        db.review.insert_one(doc)
        return(jsonify({'result':'success', 'msg':'review 저장완료'}))
    else:
        return(jsonify({'result':'fail', 'msg':'이미 작성된 review', 'data':check_reviewer[0]['review']}))



# Review_bring
@app.route('/bring_review', methods=['GET'])
def bring_review():
    ice_cream = request.args.get("ice_cream")
    bring_review_db = list(db.review.find({'ice_cream':ice_cream},{'_id':0}))
    return(jsonify({'result':'success', 'data':bring_review_db}))


if __name__ == '__main__':
    app.secret_key = 'Juni'
    app.run('localhost', port=9000, debug=True)