from urllib import request,error
import json
import socket
import time
import threading

########=========================================参数设置=============================##################

ip="localhost"
port=23333

timeout=5
report={}
mutex=threading.Lock()

Error="Error"
Failed="Failed"
Successed="Successed"

########=========================================参数设置=============================##################

socket.setdefaulttimeout(timeout)
print("#############################################################################")

nowtime=time.time()

def go_url(url,data):
    try:
        start=time.time()
        rq = request.Request(url)
        dic = json.dumps(data)
        mydata = dic.encode('utf-8')
        fopen = request.urlopen(rq, mydata)
    except error.HTTPError as e:
        print("Error:HTTPError")
        print(e.reason)
        print("请查看服务器端的错误")
        return Error
    except error.URLError as e:
        print("Error:URLError")
        print(e.reason)
        print("目测是端口或者ip不正确")
        return Error
    except socket.timeout:
        print("Error:timeout")
        print("服务器超时，当前设置的timeout为%d秒"%timeout)
        return Error

    try:
        print("访问时间:%f"%(time.time()-start))
        result = fopen.read().decode('utf-8')
        result = json.loads(result)
        return result

    except json.decoder.JSONDecodeError as e:
        print("Error:JSONDecodeError")
        print("返回的json无法加载")
        return Error
    except UnboundLocalError:
        print("访问失败")
        return Error


def MakeResult(word,testname,data=None):
    global mutex
    if(data==None):
        print(word)
        report[testname]=word
    else:
        print("%s result:" % testname)
        print(json.dumps(data))
        print(testname + " " + Successed)
        report[testname] = Successed
    print("#############################################################################")
    mutex.release()

def PrintReport():
    print("=============================================================================")
    count = 0
    print("Report:")
    for key in report:
        print(key + ":" + report[key])
        if (report[key] == Successed):
            count += 1
    print("Pass: " + str(count) + "/" + str(len(report)))
    print("=============================================================================")

def CheckDict(mydict,key):
    for i in key:
        if not mydict.__contains__(i):
            return i
    return True

###########=============上面是静态方法==============================##########
###########=============下面是各种test==============================##########

#test for url "/login"
def test_login(username,password):
    testname="test_login"
    url="http://%s:%s/login"%(ip,port)
    data={'username':username,'password':password}
    result=go_url(url,data)

    global mutex
    mutex.acquire()

    print(testname + ":")
    if(result==Error):
        MakeResult(Failed, testname)
    else:
        try:
            privilege=result["privilege"]
        except KeyError:
            print("json中无privilege的key")
            print("json:"+json.dumps(result))
            MakeResult(Failed,testname)
            return

        MakeResult(Successed,testname,result)

#test for url "/daka/banci"
def test_daka_banci(username):
    testname="test_daka_banci"
    url = "http://%s:%s/daka/banci" % (ip, port)
    data={"username":username}
    result=go_url(url,data)

    global mutex
    mutex.acquire()

    print(testname + ":")
    if (result == Error):
        MakeResult(Failed, testname)
    else:
        seek=False
        try:
            banci=result["banci"]
            if(banci!="none"):
                seek=True
        except KeyError:
            print("json中无banci的key")
            print("json:"+json.dumps(result))
            MakeResult(Failed,testname)
            return
        try:
            if(seek):
                status=result["status"]
                if(status=="finished" or status=="unfinished"):
                    MakeResult(Successed, testname, result)
                else:
                    print("status应是finished或unfinished")
                    print("json:" + json.dumps(result))
                    MakeResult(Failed, testname)
        except KeyError:
            print("json中无status的key")
            print("json:"+json.dumps(result))
            MakeResult(Failed,testname)
            return

#test for url "/daka/now"
def test_daka_now(username,banci):
    testname = "test_daka_now"
    url = "http://%s:%s/daka/now" % (ip, port)
    data = {"username": username,"banci":banci}
    result = go_url(url, data)

    global mutex
    mutex.acquire()
    print(testname + ":")
    if (result == Error):
        MakeResult(Failed, testname)
    else:
        try:
            status=result["status"]
        except KeyError:
            print("json中无status的key")
            print("json:"+json.dumps(result))
            MakeResult(Failed,testname)
            return

        MakeResult(Successed,testname,result)


#test for url "/query/month"
def test_query_month():
    testname="test_query_month"
    url = "http://%s:%s/query/month" % (ip, port)
    data={"query":"1"}
    result = go_url(url, data)

    global mutex
    mutex.acquire()
    print(testname + ":")
    if (result == Error):
        MakeResult(Failed, testname)
    else:
        try:
            month=result["month"]
            if(type(month)==type([])):
                for i in month:
                    array=i.split('.')
                    if(len(array)!=2) or not array[0].isdigit() or not array[1].isdigit():
                        print("此月份格式不对:",end=i+"\n")
                        MakeResult(Failed, testname)
                        return
            else:
                print("month的值应为list格式")
                MakeResult(Failed, testname)
                return

        except KeyError:
            print("json中无month的key")
            print("json:" + json.dumps(result))
            MakeResult(Failed, testname)
            return
        MakeResult(Successed, testname, result)


#test for url "/query/data"
def test_query_data(date):
    testname = "test_query_data"
    url = "http://%s:%s/query/data" % (ip, port)
    data = {"date": date}
    result = go_url(url, data)

    mykey=["userid","username","time","banci"]

    global mutex
    mutex.acquire()
    print(testname + ":")
    if (result == Error):
        MakeResult(Failed, testname)
    else:
        try:
            data=result['data']
            if (type(data) == type([])):
                for i in data:
                    Check=CheckDict(i,mykey)
                    if not (Check):
                        print("data中无%s的key"% Check)
                        print("json:" + json.dumps(result))
                        MakeResult(Failed, testname)
                        return

            else:
                print(type(data))
                print("data的值应为list格式")
                MakeResult(Failed, testname)
                return


        except KeyError:
            print("json中无data的key")
            print("json:" + json.dumps(result))
            MakeResult(Failed, testname)
            return
        MakeResult(Successed, testname, result)

#test for url "/query/change"
def test_query_change(userid,username,time,banci,beizhu,caozuo):
    testname = "test_query_change"
    url = "http://%s:%s/query/change" % (ip, port)
    data = {"userid": userid,"username":username,"time":time,"banci":banci,'beizhu':beizhu,"caozuo":caozuo}
    result = go_url(url, data)

    global mutex
    mutex.acquire()
    print(testname + ":")
    if (result == Error):
        MakeResult(Failed, testname)
    else:
        try:
            status=result['status']
        except KeyError:
            print("json中无status的key")
            print("json:" + json.dumps(result))
            MakeResult(Failed, testname)
            return
        MakeResult(Successed, testname, result)

#test for url "/information/password"
def test_information_password(username,oldpassword,newpassword):
    testname="test_information_password"
    url = "http://%s:%s/information/password" % (ip, port)
    data={"username":username,"oldpassword":oldpassword,"newpassword":newpassword}
    result = go_url(url, data)

    global mutex
    mutex.acquire()
    print(testname + ":")
    if (result == Error):
        MakeResult(Failed, testname)
    else:
        try:
            status=result['status']
        except KeyError:
            print("json中无status的key")
            print("json:" + json.dumps(result))
            MakeResult(Failed, testname)
            return
        MakeResult(Successed, testname, result)

#test for url "/bumen"
def test_bumen():
    testname = "test_bumen"
    url = "http://%s:%s/bumen" % (ip, port)
    data={"query":"1"}
    result=go_url(url, data)

    global mutex
    mutex.acquire()
    print(testname + ":")
    if (result == Error):
        MakeResult(Failed, testname)
    else:
        try:
            bumen=result['bumen']
            if(type(bumen)==type([])):
                if(len(bumen)<1):
                    print("无部门值")
                    MakeResult(Failed, testname)
                    return


            else:
                print("bumen的值应为list格式")
                MakeResult(Failed, testname)
                return

        except KeyError:
            print("json中无bumen的key")
            print("json:" + json.dumps(result))
            MakeResult(Failed, testname)
            return
        MakeResult(Successed, testname, result)

#test for url "/information"
def test_information(bumen):
    testname = "test_information"
    url = "http://%s:%s/information" % (ip, port)
    data = {"bumen":bumen}
    result = go_url(url, data)
    mykey=['userid','username','bumen']

    global mutex
    mutex.acquire()
    print(testname + ":")
    if (result == Error):
        MakeResult(Failed, testname)
    else:
        try:
            information=result['information']
            if(type(information)==type([])):
                for i in information:
                    Check=CheckDict(information,mykey)
                    if not (Check):
                        print("data中无%s的key" % Check)
                        print("json:" + json.dumps(result))
                        MakeResult(Failed, testname)
                        return

            else:
                print("information的值应为list格式")
                MakeResult(Failed, testname)
                return

        except KeyError:
            print("json中无information的key")
            print("json:" + json.dumps(result))
            MakeResult(Failed, testname)
            return
        MakeResult(Successed, testname, result)

#test for url "/information/change"
def test_information_change(userid,username,password,bumen,beizhu):
    testname = "test_information_change"
    url = "http://%s:%s/information/change" % (ip, port)
    data = {"userid": userid, "username": username, "password": password, "bumen": bumen,  'beizhu': beizhu}
    result = go_url(url, data)

    global mutex
    mutex.acquire()
    print(testname + ":")
    if (result == Error):
        MakeResult(Failed, testname)
    else:
        try:
            status=result['status']
        except KeyError:
            print("json中无status的key")
            print("json:" + json.dumps(result))
            MakeResult(Failed, testname)
            return
        MakeResult(Successed, testname, result)


#test for url "/banci/get"
def test_banci_get():
    testname = "test_banci_get"
    url = "http://%s:%s/banci/get" % (ip, port)
    data={"query":1}
    result = go_url(url, data)

    mykey=["username","bumen",'start','end','interval']

    global mutex
    mutex.acquire()
    print(testname + ":")
    if (result == Error):
        MakeResult(Failed, testname)
    else:
        try:
            banci=result['banci']
            if(type(banci)==type([])):
                for i in banci:
                    Check=CheckDict(banci,mykey)
                    if not(Check):
                        print("data中无%s的key" % Check)
                        print("json:" + json.dumps(result))
                        MakeResult(Failed, testname)
                        return
            else:
                print("banci的值应为list格式")
                MakeResult(Failed, testname)
                return

        except KeyError:
            print("json中无banci的key")
            print("json:" + json.dumps(result))
            MakeResult(Failed, testname)
            return
        MakeResult(Successed, testname, result)


#test for url "/banci/change"
def test_banci_change(id,bumen,start,end,interval,caozuo):
    testname = "test_banci_change"
    url = "http://%s:%s/banci/change" % (ip, port)
    data = {"id":id, "bumen": bumen, 'start': start, 'end': end, 'interval': str(interval),'caozuo':caozuo}
    result = go_url(url, data)
    global mutex
    mutex.acquire()
    print(testname + ":")
    if (result == Error):
        MakeResult(Failed, testname)
    else:
        try:
            status = result['status']
        except KeyError:
            print("json中无status的key")
            print("json:" + json.dumps(result))
            MakeResult(Failed, testname)
            return
        MakeResult(Successed, testname, result)


if __name__ == '__main__':
    TestList=[]

    TestList.append(threading.Thread(target=test_login, args=("jack", "123456")))
    #test_login(username,password)  用于测试"/login"
    TestList.append(threading.Thread(target=test_daka_banci, args=("jack",)) )
    #test_daka_banci(username)     用于测试"/daka/banci"
    TestList.append(threading.Thread(target=test_daka_now, args=("jack","2018.5.30 9:00 签到")))
    #test_daka_now(username,banci)     用于测试"/daka/now"
    TestList.append(threading.Thread(target=test_query_month) )
    #test_query_month()     用于测试"/query/month"
    TestList.append(threading.Thread(target=test_query_data,args=("2018.6.3",)  ) )
    #test_query_data(date)     用于测试"/query/data"
    TestList.append(threading.Thread(target=test_query_change, args=("110","jack","2018.5.31 8:00","2018.5.31 20:30 签退","无","delete") ) )
    # test_query_change(userid,username,time,banci,beizhu,caozuo)     用于测试"/query/change"
    TestList.append(threading.Thread(target=test_information_password,args=("jack","123456","234567")))
    # test_information_password(username,oldpassword,newpassword)     用于测试"/information/password"
    TestList.append(threading.Thread(target=test_bumen))
    # test_bumen()     用于测试"/bumen"
    TestList.append(threading.Thread(target=test_information,args=("清洁部",)))
    # test_information(bumen)   用于测试"/information"
    TestList.append(threading.Thread(target=test_information_change, args=("110","jack","123456","清洁部","无")))
    # test_information_change(userid,username,password,bumen,beizhu)   用于测试"/information/change"
    TestList.append(threading.Thread(target=test_banci_get))
    # test_banci_get() 用于测试"/banci/get"
    TestList.append(threading.Thread(target=test_banci_change, args=("admin", "清洁部", "2018.5.30 9:00", "2018.5.30 20:00", 15,'change')))
    # test_banci_change(username,bumen,start,end,interval,caozuo) 用于测试"/banci/change"



    for thread in TestList:
        thread.start()

    for thread in TestList:
        thread.join()

    PrintReport()

    print("总花费时间:"+str(time.time()-nowtime)+"秒")
