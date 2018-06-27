from flask import Flask, request, session,  redirect, url_for, abort, \
     render_template, flash,make_response,jsonify,json
from urllib import request as api,parse
import time
app=Flask(__name__)
app.config.update(dict(DEBUG=True, SECRET_KEY='Chuangxin!!!!!233', ))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config['JSON_AS_ASCII'] = False


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        myjson=json.loads(request.get_data())
        username=myjson['username']
        password=myjson['password']
        data={}
        if(username=="admin" and password=="admin"):
            data['privilege']= 2
            return jsonify(data)
        elif(password=="123456"):
            data['privilege'] = 1
            return jsonify(data)
        else:
            data['privilege'] = 0
            return jsonify(data)

@app.route('/daka/now', methods=['POST'])
def daka():
    if request.method == 'POST':
        myjson = json.loads(request.get_data())
        username=myjson['username']
        banci=myjson['banci']
        data={}
        if(banci=='2018.5.30 9:00 签到'):
            data['status']='打卡成功！'
        else:
            data['status']='打卡失败！'
        return jsonify(data)

@app.route('/daka/banci', methods=['POST'])
def getbanci():
    if request.method == 'POST':
        myjson = json.loads(request.get_data())
        username=myjson['username']
        data={}
        data['banci']='2018.5.30 9:00'
        data['status']='finished'
        return jsonify(data)

@app.route('/query/month', methods=['POST'])
def getmonth():
    if request.method == 'POST':
        myjson = json.loads(request.get_data())
        month=["2018.6","2018.4","2018.5"]
        mydict={"month":month}
        return jsonify(mydict)
@app.route('/query/data', methods=['POST'])
def getdata():
    if request.method == 'POST':
        myjson = json.loads(request.get_data())
        date=myjson['date']
        data={}
        list=[]
        dict1={'userid':"2333",'username':"jack","time":date+ " 8:00","banci":date+" 9:00 签到"}
        for  i in range(80):
            list.append(dict1)
        data['data']=list
        return jsonify(data)

@app.route('/query/change', methods=['POST'])
def querychange():
    if request.method == 'POST':
        myjson = json.loads(request.get_data())
        userid=myjson['userid']
        username=myjson['username']
        time=myjson['time']
        banci=myjson['banci']
        beizhu=myjson['beizhu']
        caozuo=myjson['caozuo']
        if(caozuo == 'delete')or (caozuo=='change') or (caozuo=='add'):
            status={'status':"成功"}
        else:
            status = {'status': "failed"}
        return jsonify(status)

@app.route('/information/password', methods=['POST'])
def changepassword():
    if request.method == 'POST':
        myjson = json.loads(request.get_data())
        oldpassword=myjson['oldpassword']
        username=myjson['username']
        newpassword = myjson['newpassword']
        if(oldpassword!=newpassword):
            status = {'status': "success"}
        else:
            status = {'status': "failed"}
        return jsonify(status)

@app.route('/bumen', methods=['POST'])
def getbumen():
    if request.method == 'POST':
        myjson = json.loads(request.get_data())
        bumen=["清洁部","死亡部","睡觉部","打牌部"]
        mydict={"bumen":bumen}
        return jsonify(mydict)

@app.route('/information', methods=['POST'])
def getinformation():
    if request.method == 'POST':
        myjson = json.loads(request.get_data())
        bumen=myjson['bumen']
        user1={'userid':"2333",'username':"jack","bumen":bumen}
        list=[]
        for i in range(20):
            list.append(user1)
        mydict={"information":list}
        return jsonify(mydict)


@app.route('/information/change', methods=['POST'])
def changeinformation():
    if request.method == 'POST':
        myjson = json.loads(request.get_data())
        userid = myjson['userid']
        username = myjson['username']
        bumen=myjson['bumen']
        password=myjson['password']
        beizhu=myjson['beizhu']
        status = {'status': "success"}
        return jsonify(status)


@app.route('/banci/get', methods=['POST'])
def banciget():
    if request.method == 'POST':
        myjson = json.loads(request.get_data())
        banci1={'id':2333, 'bumen':"清洁部",'start':"2018.5.30 9:00", 'end':"2018.5.30 20:00", 'interval':15}
        list=[]
        for i in range(10):
            list.append(banci1)

        mydict={'banci':list}
        return jsonify(mydict)

@app.route('/banci/change', methods=['POST'])
def bancichange():
    if request.method == 'POST':
        myjson = json.loads(request.get_data())
        id = myjson['id']
        bumen = myjson['bumen']
        start = myjson['start']
        end = myjson['end']
        interval = myjson['interval']
        caozuo=myjson['caozuo']
        status = {'status': "success"}
        return jsonify(status)





if __name__ == '__main__':
    app.run(host='0.0.0.0',port=23333)
