from datetime import timedelta

from flask import Flask, render_template, session, url_for, request, jsonify, app
from pymongo import MongoClient
import hashlib
import json

client = MongoClient('mongodb://bibi:6666667!@3.34.129.197', 27017)
db = client.MyPick31

app = Flask(__name__)

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
            else:
                db.userdb.insert_one({'auth_id':auth_id,'pwd':pw_hash,'nickname':nickname})
                return jsonify({'result':'success','userdb':auth_id})


# 로그인
@app.route('/customer_login', methods=['POST'])
def login():

    receive_id = request.form['receive_id']
    receive_pwd = request.form['receive_pwd']
    pwd_hash = hashlib.sha256(receive_pwd.encode('utf-8')).hexdigest()
    print(receive_id)
    print(session)
    session['email'] = receive_id
    print(session)
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

# final_flavor 전역변수 선언

#global season_final_flavor
# 최종 signature/season 정보 들어가는 변수
#bring_final_signature_db =[]
#bring_final_season_db = []

# bring_signature_db
@app.route('/bring_signature_ice_cream', methods=['POST'])
def bring_signature_ice_cream():
    # 함수 내에서 전역변수로 선언
    global signature_final_flavor
    print('////signature/////')
    receive_ice_cream = json.loads(request.form['ice_cream'])
    ice_cream = list(receive_ice_cream.values())
    # 모든 아이스크림을 가져올 때
    if ice_cream == []:
        print('모든 아이스크림 가져오기')
        bring_signature_db = list(db.signature.find({},{'_id':0}))
        return(jsonify({'result':'success_1','data':bring_signature_db}))
    #필터링으로 아이스크림을 가져올 때
    else:
        print('필터링 아이스크림 가져오기')
        # 선언한 전역변수에 빈 배열 넣기
        signature_final_flavor = []
        print(signature_final_flavor)
        temp_flavor = ice_cream[0]
        print(temp_flavor)
        for i in range(len(temp_flavor)):
            print(i)
            if i == 0 :
                print(signature_final_flavor)
                signature_filtering_cbase1(temp_flavor[i])
            if i == 1 :
                signature_filtering_cbase2(temp_flavor[i])
            if i == 2 :
                signature_filtering_ctopping1(temp_flavor[i])
            if i == 3 :
                signature_filtering_ctopping2(temp_flavor[i])
            if i == 4 :
                signature_filtering_csyrup1(temp_flavor[i])
            if i == 5 :
                signature_filtering_csyrup2(temp_flavor[i])
        print('-----------')
        #print(signature_final_flavor)
        #print(len(signature_final_flavor))

        # 중복된 flavor 제거 (list를 set 형태로 바꾼 후, 다시 list형태로 변환)
        pure_signature_final_flavor = list(set(signature_final_flavor))
        print(pure_signature_final_flavor)
        print(len(pure_signature_final_flavor))

        bring_filter_signature_db = []

        for i in range(len(pure_signature_final_flavor)):
            signature_db = list(db.signature.find({'name': pure_signature_final_flavor[i]}, {'_id': 0}))
            # 체크박스에서 선택한 요소들을 바탕으로 db에서 모두 가지는 요소의 아이스크림 가져오기
            print('비교하기!')
            print(signature_db)
            print(signature_db[0]['base'])
            ### 얘가 진또배기 ###
            print(signature_db[0]['base'].split(','))
            print(temp_flavor)
            ## 얘네 둘을 비교 ##
            print(temp_flavor[0].split(','))
            print(temp_flavor[1].split(','))

            temp = signature_db[0]['base'].split(',')
            temp1 = temp_flavor[0].split(',')
            temp2 = temp_flavor[1].split(',')
            final_temp = list()

            print('--------')
            print('검사용')
            print(temp)
            print('체크용 base1')
            print(temp1)
            print('체크용 base2')
            print(temp2)

            for flavor in temp:
                print(flavor)
                if temp1 in flavor:
                    print('존재 1')
                    print(flavor)
                    final_temp.append(flavor)
                    print(final_temp)

            for flavor in temp:
                print(flavor)
                if temp2 in flavor:
                    print('존재 2')
                    print(flavor)
                    final_temp.append(flavor)
                    print(final_temp)

            for flavor in temp2:
                print(flavor)
                if temp in flavor:
                    print('존재 3')
                    print(flavor)
                    final_temp.append(flavor)
                    print(final_temp)

            #if(signature_db[0]['base'] != ""):
                # base 값이 temp_flavor 에 있을 때
                #if(temp_flavor[0].split(',') in signature_db[0]['base'].split(',')) or (temp_flavor[1].split(',') in signature_db[0]['base'].split(',')):
                    # topping 값이 있을 때
                    #print('====')
                    #print(temp_flavor[0] in signature_db[0]['base'].split(','))
                    #print(temp_flavor[1] in signature_db[0]['base'].split(','))
                    #if (signature_db[0]['topping'] != ""):
                        # topping 값이 temp_flavor에 있을 때
                        #if (temp_flavor[2] in signature_db[0]['topping'].split(',')) or (temp_flavor[3] in signature_db[0]['topping'].split(',')):
                            #print('$$$$')
                            #print(temp_flavor[2] in signature_db[0]['topping'].split(','))
                            #print(temp_flavor[3] in signature_db[0]['topping'].split(','))
                            # syrup 값이 있을 때
                            #if (signature_db[0]['syrup'] != ""):
                                # syrup 값이 temp_flavor에 있을 때
                                #if (temp_flavor[4] in signature_db[0]['syrup'].split(',')) or (temp_flavor[5] in
                                        #signature_db[0]['syrup'].split(',')):
                                    # bring_filter_signature_db 변수에 append 하기
                                    #print('****')
                                    #print(temp_flavor[4] in signature_db[0]['syrup'].split(','))
                                    #print(temp_flavor[5] in
                                        #signature_db[0]['syrup'].split(','))
                                    #print('최종!')
                                    #print(signature_db)
                                    #bring_filter_signature_db.append(signature_db)
                                #else:
                                    #print('겹치는 syrup가 없습니다.')
                            #syrup 값이 없을 때
                            #else:
                                #print('syrup이 빈 값!')
                        # topping 값이 temp_flavor에 없을 때
                        #else:
                            #print('겹치는 topping이 없습니다.')
                    # topping 값이 없을 때
                    #else:
                        #print('topping이 빈 값!')
                # base 값이 temp_flavor 에 없을 때
                #else:
                    #print('====')
                    #temp1 = temp_flavor[0].split(',') in signature_db[0]['base'].split(',')
                    #print(temp1)
                    #temp2 = temp_flavor[1].split(',') in signature_db[0]['base'].split(',')
                    #print(temp2)
                    #temp3 = list(set(temp))
                    #print('겹치는 base가 없습니다.')
            # base 값이 없을 때
            #else:
                #print('base가 빈 값!')

        print('★signature 최종결과★')
        print(bring_filter_signature_db)
        print(len(bring_filter_signature_db))

        return(jsonify({'result':'success_2', 'data': bring_filter_signature_db}))

###signature 필터링에 사용되는 함수###

# signature를 할때 사용할 filter 함수와 season을 할 때 사용할 filter 함수 별도로 존재해야함.

def signature_filtering_cbase1(flavor):
    print(signature_final_flavor)
    print(flavor)
    # cbase1 값이 없을 때
    if flavor == "":
        print('base1 없어!')
        pass
    # cbase1 값이 있을 때
    elif flavor != "":
        cbase1 = list(db.signature.find({'base':{'$regex': flavor}},{'_id':0}))
        for i in range(len(cbase1)):
            cbase1_name = cbase1[i]['name']
            signature_final_flavor.append(cbase1_name)
        print(signature_final_flavor)
        return signature_final_flavor

# cbase2 는 여러개의 정보가 들어갈 수 있기 때문에 for문이 들어가야함.
def signature_filtering_cbase2(flavor):
    print(signature_final_flavor)
    print(flavor)
    #cbase2 값이 없을 때
    if flavor == "":
        print('base2 없어!')
        pass
    # cbase2 값이 있을 때
    elif flavor != "":
        receive_flavor = flavor.split(',')
        for i in range(len(receive_flavor)):
            cbase2 = list(db.signature.find({'base':{'$regex': receive_flavor[i]}},{'_id':0}))
            for j in range(len(cbase2)):
                cbase2_name = cbase2[j]['name']
                signature_final_flavor.append(cbase2_name)
            print(signature_final_flavor)
        return signature_final_flavor

def signature_filtering_ctopping1(flavor):
    print(signature_final_flavor)
    print(flavor)
    if flavor == "":
        print('topping1 없어!')
        pass
    elif flavor != "":
        ctopping1 = list(db.signature.find({'topping':{'$regex': flavor}},{'_id': 0}))
        for i in range(len(ctopping1)):
            ctopping1_name = ctopping1[i]['name']
            #print(ctopping1_name)
            signature_final_flavor.append(ctopping1_name)
            #print(signature_final_flavor)
        print(signature_final_flavor)
        return signature_final_flavor

def signature_filtering_ctopping2(flavor):
    print(signature_final_flavor)
    print(flavor)
    if flavor == "":
        print('topping2 없어!')
        pass
    elif flavor != "":
        receive_flavor = flavor.split(',')
        for i in range(len(receive_flavor)):
            ctopping2 = list(db.signature.find({'topping': {'$regex': receive_flavor[i]}}, {'_id': 0}))
            for j in range(len(ctopping2)):
                ctopping2_name = ctopping2[j]['name']
                signature_final_flavor.append(ctopping2_name)
        return signature_final_flavor

def signature_filtering_csyrup1(flavor):
    print(signature_final_flavor)
    print(flavor)
    if flavor == "":
        print('syrup1 없어!')
        pass
    elif flavor != "":
        csyrup1 = list(db.signature.find({'syrup':{'$regex': flavor}}, {'_id': 0}))
        for i in range(len(csyrup1)):
            csyrup1_name = csyrup1[i]['name']
            signature_final_flavor.append(csyrup1_name)
        print(signature_final_flavor)
        return signature_final_flavor

def signature_filtering_csyrup2(flavor):
    print(signature_final_flavor)
    print(flavor)
    if flavor == "":
        print('syrup2 없어!')
        pass
    elif flavor != "":
        receive_flavor = flavor.split(',')
        for i in range(len(receive_flavor)):
            csyrup2 = list(db.signature.find({'syrup': {'$regex': receive_flavor[i]}}, {'_id': 0}))
            for j in range(len(csyrup2)):
                csyrup2_name = csyrup2[j]['name']
                signature_final_flavor.append(csyrup2_name)
            print(signature_final_flavor)
        return signature_final_flavor

########################################

# bring_season_db
@app.route('/bring_season_ice_cream', methods=['POST'])
def bring_season_ice_cream():
    # 함수 내에서 전역변수로 선언
    global season_final_flavor
    print('/////season//////')
    receive_ice_cream = json.loads(request.form['ice_cream'])
    ice_cream = list(receive_ice_cream.values())
    # 모든 아이스크림을 가져올 때
    if ice_cream == []:
        print('모든 아이스크림 가져오기')
        bring_season_db = list(db.season.find({}, {'_id': 0}))
        return (jsonify({'result': 'success_1', 'data': bring_season_db}))
    # 필터링으로 아이스크림을 가져올 때
    else:
        print('필터링 아이스크림 가져오기')
        # 선언한 전역변수에 빈 배열 넣기
        season_final_flavor = []
        temp_flavor = ice_cream[0]
        #print(temp_flavor)
        for i in range(len(temp_flavor)):
            if i == 0:
                season_filtering_cbase1(temp_flavor[i])
            if i == 1:
                season_filtering_cbase2(temp_flavor[i])
            if i == 2:
                season_filtering_ctopping1(temp_flavor[i])
            if i == 3:
                season_filtering_ctopping2(temp_flavor[i])
            if i == 4:
                season_filtering_csyrup1(temp_flavor[i])
            if i == 5:
                season_filtering_csyrup2(temp_flavor[i])
        print('-----------')
        print(season_final_flavor)
        print(len(season_final_flavor))

        # 중복된 flavor 제거 (list를 set 형태로 바꾼 후, 다시 list형태로 변환)
        pure_season_final_flavor = list(set(season_final_flavor))
        print(pure_season_final_flavor)
        print(len(pure_season_final_flavor))

        bring_filter_season_db = []

        #bring_pure_season_final_flavor_data(pure_season_final_flavor)

        for i in range(len(pure_season_final_flavor)):
            #print(pure_season_final_flavor[i])
            season_db = list(db.season.find({'name': pure_season_final_flavor[i]}, {'_id': 0}))
            bring_filter_season_db.append(season_db)

        print('★season 최종결과★')
        print(bring_filter_season_db)
        print(len(bring_filter_season_db))

        return (jsonify({'result': 'success_2', 'data': bring_filter_season_db}))



####season 필터링에 사용되는 함수#####

def season_filtering_cbase1(flavor):
    print(season_final_flavor)
    print(flavor)
    # cbase1 값이 없을 때
    if flavor == "":
        print('base1 없어!')
        pass
    # cbase1 값이 있을 때
    elif flavor != "":
        cbase1 = list(db.season.find({'base': {'$regex': flavor}}, {'_id': 0}))
        for i in range(len(cbase1)):
            cbase1_name = cbase1[i]['name']
            season_final_flavor.append(cbase1_name)
        print(season_final_flavor)
        return season_final_flavor

# cbase2 는 여러개의 정보가 들어갈 수 있기 때문에 for문이 들어가야함.
def season_filtering_cbase2(flavor):
    print(season_final_flavor)
    print(flavor)
    # cbase2 값이 없을 때
    if flavor == "":
        print('base2 없어!')
        pass
    # cbase2 값이 있을 때
    elif flavor != "":
        receive_flavor = flavor.split(',')
        for i in range(len(receive_flavor)):
            cbase2 = list(db.season.find({'base': {'$regex': receive_flavor[i]}}, {'_id': 0}))
            for j in range(len(cbase2)):
                cbase2_name = cbase2[j]['name']
                season_final_flavor.append(cbase2_name)
            print(season_final_flavor)
        return season_final_flavor

def season_filtering_ctopping1(flavor):
    print(season_final_flavor)
    print(flavor)
    if flavor == "":
        print('topping1 없어!')
        pass
    elif flavor != "":
        ctopping1 = list(db.season.find({'topping': {'$regex': flavor}}, {'_id': 0}))
        for i in range(len(ctopping1)):
            ctopping1_name = ctopping1[i]['name']
            # print(ctopping1_name)
            season_final_flavor.append(ctopping1_name)
            # print(signature_final_flavor)
        print(season_final_flavor)
        return season_final_flavor

def season_filtering_ctopping2(flavor):
    print(season_final_flavor)
    print(flavor)
    if flavor == "":
        print('topping2 없어!')
        pass
    elif flavor != "":
        receive_flavor = flavor.split(',')
        for i in range(len(receive_flavor)):
            ctopping2 = list(db.season.find({'topping': {'$regex': receive_flavor[i]}}, {'_id': 0}))
            for j in range(len(ctopping2)):
                ctopping2_name = ctopping2[j]['name']
                season_final_flavor.append(ctopping2_name)
        return season_final_flavor

def season_filtering_csyrup1(flavor):
    print(season_final_flavor)
    print(flavor)
    if flavor == "":
        print('syrup1 없어!')
        pass
    elif flavor != "":
        csyrup1 = list(db.season.find({'syrup': {'$regex': flavor}}, {'_id': 0}))
        for i in range(len(csyrup1)):
            csyrup1_name = csyrup1[i]['name']
            season_final_flavor.append(csyrup1_name)
        print(season_final_flavor)
        return season_final_flavor

def season_filtering_csyrup2(flavor):
    print(season_final_flavor)
    print(flavor)
    if flavor == "":
        print('syrup2 없어!')
        pass
    elif flavor != "":
        receive_flavor = flavor.split(',')
        for i in range(len(receive_flavor)):
            csyrup2 = list(db.season.find({'syrup': {'$regex': receive_flavor[i]}}, {'_id': 0}))
            for j in range(len(csyrup2)):
                csyrup2_name = csyrup2[j]['name']
                season_final_flavor.append(csyrup2_name)
            print(season_final_flavor)
        return season_final_flavor


#####################
##아이스크림필터링-bibi#
#####################
# 체크한 베이스로 필터링
@app.route('/checkBase', methods=["POST"])
def checkBase():
    # from ajax
    sendBases = json.loads(request.form["sendBases"])
    checkedBasesList = sendBases['checkedBases']
    cbaseList = [] # 배열? 딕셔너리? 배열이 더 나을 것 같은데.

    for i in range(len(checkedBasesList)): # 베이스배열 요소 하나씩 입(출)력. i = 체크된 cbase1
        # from mongoDB
        cbaseList.append(list(db.cbase.find({"cbase1": checkedBasesList[i]}, {'_id': 0})))

    return (jsonify({'result': 'success', 'msg': "서버와 연결되었음-베이스", 'data':cbaseList}))

# 체크한 토핑으로 필터링
@app.route('/checkTopping', methods=["POST"])
def checkTopping():
    # from ajax
    sendToppings = json.loads(request.form["sendToppings"])
    checkedToppingsList = sendToppings['checkedToppings']
    ctoppingList = [] # 배열? 딕셔너리? 배열이 더 나을 것 같은데.

    for i in range(len(checkedToppingsList)): # 베이스배열 요소 하나씩 입(출)력. i = 체크된 cbase1
        # from mongoDB
        ctoppingList.append(list(db.ctopping.find({"ctopping1": checkedToppingsList[i]}, {'_id': 0})))

    return (jsonify({'result': 'success', 'msg': "서버와 연결되었음-베이스", 'data':ctoppingList}))

# 체크한 시럽으로 필터링
@app.route('/checkSyrup', methods=["POST"])
def checkSyrup():
    # from ajax
    sendSyrups = json.loads(request.form["sendSyrups"])
    checkedSyrupsList = sendSyrups['checkedSyrups']
    csyrupList = [] # 배열? 딕셔너리? 배열이 더 나을 것 같은데.

    for i in range(len(checkedSyrupsList)):
        # from mongoDB
        csyrupList.append(list(db.csyrup.find({"csyrup1": checkedSyrupsList[i]}, {'_id': 0})))

    return (jsonify({'result': 'success', 'msg': "서버와 연결되었음-베이스", 'data':csyrupList}))

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