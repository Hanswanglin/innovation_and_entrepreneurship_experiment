from flask import Flask, request, session,  redirect, url_for, abort, \
     render_template, flash,make_response,jsonify,json
from flask_cors import CORS
from urllib import request as api,parse
import time
import Caculate
app=Flask(__name__)
app.config.update(dict(DEBUG=True, SECRET_KEY='Chuangxin!!!!!233', ))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
CORS(app, supports_credentials=True)
ip="localhost"
port=8000
pageoffset=9
firstpage=1
maxshow=5
url_login="http://%s:%s/login" %(ip,port)
url_data = "http://%s:%s/query/data"% (ip,port)
url_month= "http://%s:%s/query/month"% (ip,port)
url_change_history="http://%s:%s/query/change"% (ip,port)
url_daka='http://%s:%s/daka/' %(ip,port)
url_bumen='http://%s:%s/bumen' %(ip,port)
url_information='http://%s:%s/information' %(ip,port)
url_change_information='http://%s:%s/information/change2' %(ip,port)
url_change_password='http://%s:%s/information/password'%(ip,port)
url_banci_get='http://%s:%s/banci/get'%(ip,port)
url_banci_change='http://%s:%s/banci/change'%(ip,port)

sidebar=[{'name':'今日打卡详情','href':'/today'},{'name':'打卡历史记录','href':'/history'},
         {'name': '员工信息管理', 'href': '/information'},{'name': '班次设置', 'href': '/banci'}]

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None


    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        data={'username':username,'password':password}
        result=GetData(url_login,data)

        try:
            result=json.loads(result)
            privilege=int(result['privilege'])
            if(privilege==0):
                session.clear()
                error='用户名或密码错误'
                return render_template('login.html', error=error)
            elif(privilege  ==  1):
                session['login'] = True
                session['username'] = username
                session['privilege'] = privilege
                return redirect(url_for('daka'))
            elif (privilege == 2):
                session['login']=True
                session['username']=username
                session['privilege']=privilege
                return redirect(url_for('today'))


        except:
            print("load json error")
            error = "服务器出现错误"
            session.clear()
            return render_template('login.html', error=error)

    if(session.get('login')) and session.get('username') and session.get('privilege'):
        if session['privilege']==1:
            return redirect(url_for('daka'))
        elif session['privilege']==2:
            return redirect(url_for('today'))

    return  render_template('login.html', error=error)

@app.route('/daka', methods=['GET', 'POST'])
def daka():
    url = url_daka

    if request.method == 'POST':
        try:
            myjson=json.loads(request.get_data())
            username=myjson['username']
            banci=myjson['banci']
            data={'username':username,'banci':banci}
            myurl=url+'now'
            result=GetData(myurl,data)
            return result
        except:
            return jsonify({'status':'Failed'})

    if(session.get('login') and session.get('username') and session.get('privilege') ):
        if(session['privilege']==2):
            return redirect(url_for('Today'))
    else:
        session.clear()
        return redirect(url_for('login'))

    myurl=url+'banci'
    username=session['username']
    data={'username':username}
    result=GetData(myurl,data)
    try:
        mydict=json.loads(result)
        banci=mydict['banci']
        status=mydict['status']
        if(banci!='none'):
            if(status=='unfinished'):
                return render_template('daka.html', name=username, banci=banci)
            elif(status=='finished'):
                return render_template('daka.html', name=username, banci=banci,button="打卡完成")
        else:
            return render_template('daka.html', name=username, banci=banci, button="无需打卡")
    except:
        return redirect(url_for("Error"))


@app.route('/today', methods=['GET', 'POST'])
def today():
    if(session.get('login') and session.get('username') and session.get('privilege') ):
        if(session['privilege']==1):
            return redirect(url_for('daka'))
    else:
        session.clear()
        return redirect(url_for('login'))
    username=session['username']

    page=int(request.args.get("p",1))

    date=time.strftime("%Y.%m.%d")
    data = {"date": date}
    result = GetData(url_data, data)
    result=json.loads(result)
    data = result['data']
    mydata = Caculate.GetPageDict(page,data,pageoffset,maxshow)
    return render_template('Today.html', data=mydata,username=username,sidebar=sidebar,active='今日打卡详情')

@app.route('/history', methods=['GET', 'POST'])
def history():
    if (session.get('login') and session.get('username') and session.get('privilege')):
        if (session['privilege'] == 1):
            return redirect(url_for('daka'))
    else:
        session.clear()
        return redirect(url_for('login'))
    username = session['username']

    page = int(request.args.get("p", 1))
    date = request.args.get("date", time.strftime("%Y.%m.%d"))

    data={'query':'1'}
    result = GetData(url_month, data)
    result = json.loads(result)
    data=result['month']
    start=Caculate.getstartmonth(data)
    date1=Caculate.changedate(date)
    data = {"date": date1}
    result = GetData(url_data, data)
    result = json.loads(result)
    data=result['data']
    mydata = Caculate.GetPageDict(page, data, pageoffset-1, maxshow)

    return render_template('History.html', data=mydata,date=date,start=start,username=username,sidebar=sidebar,active='打卡历史记录')


@app.route('/change/history', methods=['POST'])
def change_history():

    if request.method == 'POST':
        if (session.get('login') and session.get('username') and session.get('privilege')):
            pass
        else:
            return jsonify({'status': '请关闭浏览器重新登录'})
        try:
            myjson=json.loads(request.get_data())
            userid=myjson['id']
            username=myjson['name']
            banci=myjson['banci']
            time=myjson['time']
            beizhu=myjson['beizhu']
            caozuo=myjson['caozuo']
            data={'userid':userid,'username':username,'banci':banci,'beizhu':beizhu,'caozuo':caozuo,'time':time}
            result=GetData(url_change_history,data)
            return result
        except:
            return jsonify({'status':'Failed'})


@app.route('/information', methods=['GET','POST'])
def information():
    if request.method == 'POST':
        try:
            if (session.get('login') and session.get('username') and session.get('privilege')):
                pass
            else:
                return jsonify({'status': '请关闭浏览器重新登录'})
            myjson=json.loads(request.get_data())
            userid=myjson['id']
            username=myjson['name']
            bumen=myjson['bumen']
            beizhu=myjson['beizhu']
            caozuo=myjson['caozuo']
            if not myjson.__contains__('password'):
                password=""
            else:
                password=myjson['password']
            data={'userid':userid,'username':username,'bumen':bumen,'beizhu':beizhu,'caozuo':caozuo,'password':password}
            result=GetData(url_change_information,data)
            return result
        except:
            return jsonify({'status':'Failed'})

    if (session.get('login') and session.get('username') and session.get('privilege')):
        if (session['privilege'] == 1):
            return redirect(url_for('daka'))
    else:
        session.clear()
        return redirect(url_for('login'))
    username = session['username']

    data={'query':'1'}
    result = GetData(url_bumen, data)
    result = json.loads(result)
    allbumen = result['bumen']
    firstbumen=allbumen[0]

    page = int(request.args.get("p", 1))
    nowbumen = request.args.get("bumen",firstbumen)
    data={'bumen':nowbumen}
    result = GetData(url_information, data)
    result = json.loads(result)
    data = result['information']
    mydata = Caculate.GetPageDict(page, data, pageoffset - 2, maxshow)
    return render_template('Information.html', data=mydata, username=username,nowbumen=nowbumen,allbumen=allbumen,sidebar=sidebar,active="员工信息管理")


@app.route('/myinformation', methods=['GET','POST'])
def myinformation():
    if request.method == 'POST':
        if (session.get('login') and session.get('username') and session.get('privilege')):
            pass
        else:
            return jsonify({'status': '请关闭浏览器重新登录'})
        myjson = json.loads(request.get_data())
        username=myjson['username']
        oldpassword=myjson['oldpassword']
        newpassword=myjson['newpassword']
        data={'username':username,'oldpassword':oldpassword,'newpassword':newpassword}
        result = GetData(url_change_password, data)
        return result

    if (session.get('login') and session.get('username') and session.get('privilege')):
        if (session['privilege'] == 1):
            return redirect(url_for('daka'))
    else:
        session.clear()
        return redirect(url_for('login'))
    username = session['username']

    return render_template('My_Information.html', username=username,sidebar=sidebar)

@app.route('/banci', methods=['GET','POST'])
def banci():
    if request.method == 'POST':
        if (session.get('login') and session.get('username') and session.get('privilege')):
            pass
        else:
            return jsonify({'status': '请关闭浏览器重新登录'})
        myjson = json.loads(request.get_data())
        result = GetData(url_banci_change, myjson)
        return result



    if (session.get('login') and session.get('username') and session.get('privilege')):
        if (session['privilege'] == 1):
            return redirect(url_for('daka'))
    else:
        session.clear()
        return redirect(url_for('login'))
    username = session['username']

    data={'query':'1'}
    result=GetData(url_banci_get,data)
    result=json.loads(result)
    allbanci=result['banci']

    page = int(request.args.get("p", 1))
    mydata = Caculate.GetPageDict(page, allbanci, pageoffset - 1, maxshow)
    return render_template('Banci.html', data=mydata, username=username,sidebar=sidebar,active='班次设置')




@app.route('/out')
def out():
    session.clear()
    return redirect(url_for('login'))

@app.route('/Error')
def Error():
    return "服务器出错，请稍后再试"

def GetData(url,data=None):
    if(data!=None):
        Nowdata=json.dumps(data)
        Nowdata=Nowdata.encode('utf-8')
        NowRequest = api.Request(url)
        f=api.urlopen(NowRequest,Nowdata)
    else:
        NowRequest = api.Request(url)
        f = api.urlopen(NowRequest)
    return f.read().decode('utf-8')





if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)