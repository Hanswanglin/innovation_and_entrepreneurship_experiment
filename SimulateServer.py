from flask import Flask, request, session,  redirect, url_for, abort, \
     render_template, flash,make_response,jsonify,json
from urllib import request as api,parse
import datetime

from Link_db import Link_db
app=Flask(__name__)
app.config.update(dict(DEBUG=True, SECRET_KEY='Chuangxin!!!!!233', ))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config['JSON_AS_ASCII'] = False


@app.route('/login', methods=['POST'])
def login():
    db = Link_db()
    if request.method == 'POST':
        myjson = json.loads(request.get_data())
        username = myjson['username']
        password = myjson['password']
        sql = "select * from users where user_name=\"" + username + "\""
        result = db.select(sql)

        data={}
        if (len(result) == 0):
            data['privilege'] = 0
            return jsonify(data)
        elif (password == result[0][3]):
            data['privilege'] = result[0][4]
            return jsonify(data)
        else:
            data['privilege'] = 0
            return jsonify(data)

@app.route('/daka/now', methods=['POST'])
def daka():
    if request.method == 'POST':
        myjson = json.loads(request.get_data())
        username = myjson['username']
        this_banci = myjson['banci']
        data = {}

        localtime = datetime.datetime.now()
        db = Link_db()

        # 获取员工部门信息
        sql = "select * from users where user_name=\"" + username + "\""
        users_data = db.select(sql)
        id = users_data[0][1]
        bumen = users_data[0][5]
        # 获取部门的班次信息
        sql = "select * from banci_info where bumen=\"" + bumen + "\""
        banci_data = db.select(sql)
        # check当前时间是否在可打卡的时间里;如果在，则打卡成功.
        banci_info = "none"
        for i in range(len(banci_data)):
            s = banci_data[i][1]
            e = banci_data[i][2]
            star = datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
            end = datetime.datetime.strptime(e, '%Y-%m-%d %H:%M:%S')
            interval = banci_data[i][3]
            clock_status = '打卡失败！'
            if datetime.datetime.strptime(this_banci, '%Y-%m-%d %H:%M:%S') == star:
                if star - datetime.timedelta(minutes=interval) < localtime < star:
                    clock_status = '打卡成功！'
                    banci_info = s + " 签到"
                    break
            elif datetime.datetime.strptime(this_banci, '%Y-%m-%d %H:%M:%S') == end:
                if end < localtime < end + datetime.timedelta(minutes=interval):
                    clock_status = '打卡成功！'
                    banci_info = e + " 签退"
                    break
        data['status'] = clock_status
        # 打卡成功，向clock_info插入一条新数据。
        if clock_status == '打卡成功！':
            sql = "insert into clock_info (user_id,Clock_time,banci) values (\"" + id + "\",\"" + localtime.strftime(
                "%Y-%m-%d %H:%M:%S") + "\",\"" + banci_info + "\")"
            affect = db.update(sql)
        return jsonify(data)

@app.route('/daka/banci', methods=['POST'])
def getbanci():
    if request.method == 'POST':
        myjson = json.loads(request.get_data())
        username = myjson['username']
        data = {}

        localtime = datetime.datetime.now()
        db = Link_db()

        # 获取员工部门信息
        sql = "select * from users where user_name=\"" + username + "\""
        users_data = db.select(sql)
        id = users_data[0][1]
        bumen = users_data[0][5]
        # 获取部门的班次信息
        sql = "select * from banci_info where bumen=\"" + bumen + "\""
        banci_data = db.select(sql)
        # 获取打卡信息表里该员工的所有记录
        sql = "select * from clock_info where user_id=\"" + id + "\""
        clock_data = db.select(sql)
        # check当前时间是否在可打卡的时间里
        banci = "none"
        for i in range(len(banci_data)):
            s = banci_data[i][1]
            e = banci_data[i][2]
            star = datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
            end = datetime.datetime.strptime(e, '%Y-%m-%d %H:%M:%S')
            interval = banci_data[i][3]
            if star - datetime.timedelta(minutes=interval) < localtime < star:
                banci = s
                break
            elif end < localtime < end + datetime.timedelta(minutes=interval):
                banci = e
                break
        # 如果在可打卡的时间里，check是否已完成打卡
        status = "unfinished"
        if banci != "none":
            for i in range(len(clock_data)):
                print(clock_data[i][2])
                clockTime = datetime.datetime.strptime(clock_data[i][2], '%Y-%m-%d %H:%M:%S')
                if (star - datetime.timedelta(minutes=interval) < clockTime < star) or (
                                end < clockTime < end + datetime.timedelta(minutes=interval)):
                    status = "finished"
        data['banci'] = banci
        data['status'] = status
        return jsonify(data)

# 打卡历史记录界面获取可以查询的月份
@app.route('/query/month', methods=['POST'])
def getmonth():
    db = Link_db()

    if request.method == 'POST':
        sql = "select strftime('%Y.%m', Clock_time) as month from clock_info group by month"
        result = db.select(sql)
        print(result)
        month = []
        for m in range(len(result)):
            month.append(result[m][0])

        myjson = json.loads(request.get_data())
        mydict={"month":month}
        return jsonify(mydict)

# 按照日期查询所有数据
@app.route('/query/data', methods=['POST'])
def getdata():
    if request.method == 'POST':
        myjson = json.loads(request.get_data())
        date=myjson['date'] #2018.05.31
        data={}
        list=[]
        db = Link_db()
        sql = "select * from clock_info where Clock_time like \"" + date + "%\""
        result1 = db.select(sql)

        for r in range(len(result1)):# 搜出来的数据量
            record = {}
            record["userid"] = result1[r][1]# 员工编号
            sql2 = "select user_name from users where user_id = \"" + record["userid"] + "\""
            user_name = db.select(sql2)
            record["username"] = user_name[0][0]
            record["time"] = result1[r][2]
            record["banci"] = result1[r][3]
            list.append(record)
        data['data']=list
        return jsonify(data)


@app.route('/query/change', methods=['POST'])
def querychange():
    if request.method == 'POST':
        myjson = json.loads(request.get_data())
        userid = myjson['userid']
        username = myjson['username']
        time = myjson['time']
        banci = myjson['banci']
        beizhu = myjson['beizhu']
        caozuo = myjson['caozuo']

        db = Link_db()
        if (caozuo == 'delete'):
            sql1 = "delete from clock_info where user_id=\"" + userid + "\" and Clock_time=\"" + time + "\""
            db.update(sql1)
            status = {'status': "success"}
        elif (caozuo == 'change'):
            ##只能根据userid和banci更改time
            sql1 = "update clock_info set  Clock_time=\"" + time + "\" where user_id=\"" + userid + "\" and banci=\"" + banci + "\""
            db.update(sql1)
            status = {'status': "success"}
        elif (caozuo == 'add'):
            sql1 = "insert into clock_info(user_id,Clock_time,banci) values(\"" + userid + "\",\"" + time + "\",\"" + banci + "\")"
            db.update(sql1)
            status = {'status': "success"}
        else:
            status = {'status': "failed"}

        return jsonify(status)

@app.route('/information/password', methods=['POST'])
def changepassword():
    if request.method == 'POST':
        myjson = json.loads(request.get_data())
        oldpassword = myjson['oldpassword']
        username = myjson['username']
        newpassword = myjson['newpassword']

        # 先查询是否原密码正确
        db = Link_db()
        sql3 = "select * from users where user_name=\"" + username + "\""
        result2 = db.select(sql3)
        passwprd = str(result2[0][3])
        if (oldpassword == passwprd):  # 再进行修改
            sql = "update users set password=" + newpassword + " where user_name=\"" + username + "\""
            result = db.update(sql)
            status = {'status': "success"}
        else:  # 旧密码不匹配
            status = {'status': "failed"}
        return jsonify(status)

@app.route('/bumen', methods=['POST'])
def getbumen():
    if request.method == 'POST':
        myjson = json.loads(request.get_data())
        db = Link_db()
        sql = "select * from users group by staff_bumen"
        result = db.select(sql)
        bumen = []
        for x in result:
            if (x[5] != None):
                bumen.append(x[5])

        mydict = {"bumen": bumen}
        return jsonify(mydict)

@app.route('/information', methods=['POST'])
def getinformation():
    if request.method == 'POST':
        myjson = json.loads(request.get_data())
        bumen = myjson['bumen']

        if (bumen == "none"):  # 返回所有员工信息
            list = []
            db = Link_db()
            sql = "select * from users"
            result = db.select(sql)
            list = []
            for x in result:
                user = {}
                user["userid"] = x[1]
                user["username"] = x[2]
                user["bumen"] = x[5]
                list.append(user)

        else:  # 返回相关部门员工信息
            db = Link_db()
            sql = "select * from users where staff_bumen=\"" + bumen + "\""
            result = db.select(sql)
            list = []
            for x in result:
                user = {}
                user['userid'] = x[1]
                user['username'] = x[2]
                user['bumen'] = x[5]
                list.append(user)

        mydict = {"information": list}
        return jsonify(mydict)


@app.route('/information/change', methods=['POST'])
def changeinformation():
    if request.method == 'POST':
        myjson = json.loads(request.get_data())
        userid = myjson['userid']
        username = myjson['username']
        bumen = myjson['bumen']
        password = myjson['password']
        beizhu = myjson['beizhu']

        # 进行修改
        db = Link_db()
        if (password == ''):
            sql = "update users set staff_bumen=\"" + bumen + "\" where user_id=" + userid
            result = db.update(sql)
        else:
            sql = "update users set staff_bumen=\"" + bumen + "\",password=\"" + password + "\" where user_id=" + userid
            result = db.update(sql)

        status = {'status': "success"}
        return jsonify(status)

#  备用，全面的
@app.route('/information/change2', methods=['POST'])
def changeinformation2():
    if request.method == 'POST':
        myjson = json.loads(request.get_data())
        userid = myjson['userid']
        username = myjson['username']
        bumen = myjson['bumen']
        password = myjson['password']
        beizhu = myjson['beizhu']
        caozuo = myjson['caozuo']

        db = Link_db()
        if (caozuo == "add"):  # 进行增加
            sql = "insert into users(user_id,user_name,staff_bumen,password,role) values(\"" + userid + "\",\"" + username + "\",\"" + bumen + "\",\"" + password + "\",1)"
            db.update(sql)
            status = {'status': "added"}
        elif (caozuo == "change"):  # 修改，会看一下password对不对

            if (password == ''):
                sql = "update users set staff_bumen=\"" + bumen + "\" where user_id=" + userid
                db.update(sql)
            else:
                sql = "update users set staff_bumen=\"" + bumen + "\",password=\"" + password + "\" where user_id=" + userid
                db.update(sql)
            status = {'status': "changed"}
        elif (caozuo == "delete"):
            sql = "delete from users where user_id=" + userid
            db.update(sql)
            status = {'status': "deleted"}

        status = {'status': "success"}
        return jsonify(status)


@app.route('/banci/get', methods=['POST'])
def banciget():
    if request.method == 'POST':
        myjson = json.loads(request.get_data())

        db = Link_db()
        sql = "select * from banci_info"
        result = db.select(sql)
        print(result)
        print("\n")
        list = []
        for x in result:
            banci = {}
            banci['id'] = str(x[0])
            banci['bumen'] = x[4]
            banci['start'] = x[1]
            banci['end'] = x[2]
            banci['interval'] = str(x[3])
            list.append(banci)
        print(list)
        mydict = {'banci': list}

        return jsonify(mydict)

@app.route('/banci/change', methods=['POST'])
def bancichange():
    if request.method == 'POST':
        myjson = json.loads(request.get_data())

        bumen = myjson['bumen']
        start = myjson['start']
        end = myjson['end']
        interval = myjson['interval']
        caozuo = myjson['caozuo']

        db = Link_db()
        if (caozuo == "change"):  # 改动
            id = myjson['id']
            sql = "update banci_info set bumen=\"" + bumen + "\",start=\"" + start + "\",end=\"" + end + "\",interval=\"" + interval + "\"  where banci_id=" + id
            db.update(sql)

        elif (caozuo == "delete"):  # 删除
            id = myjson['id']
            sql = "delete from banci_info where banci_id=" + id
            db.update(sql)

        elif (caozuo == "add"):  # 增加
            sql = "insert into banci_info(start,end,interval,bumen) values(\"" + start + "\",\"" + end + "\"," + interval + ",\"" + bumen + "\")"
            db.update(sql)

        status = {'status': 'success'}
        return jsonify(status)


if __name__ == '__main__':
    # app.run(host='0.0.0.0',port=23333)
    app.run(debug=True, port=8000)