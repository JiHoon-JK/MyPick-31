from pymongo import MongoClient
client = MongoClient('localhost',27017)
db = client.MyPick31

from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/createCB', methods=['POST'])
def createCB():
    cbase1 = request.form['cbase1']
    cbase2 = request.form['cbase2']
    doc ={
        'cbase1': cbase1,
        'cbase2': cbase2
    }
    db.cbase.insert_one(doc)
    return jsonify({'result' : 'success' , 'msg' : 'cbase에 저장완료'});


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)