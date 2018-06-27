def GetPageDict(nowpage, data,pageoffset,maxshow):
    #nowpage 当前页 data 数据 pageoffset 每页最多条数 maxshow 显示出来的页数
    mydict = {}

    total = len(data) / pageoffset
    if (total > int(total)):
        total = int(total) + 1
    total = int(total)
    # 向上取整

    mydict['total'] = total
    mydict['nowpage'] = nowpage
    if (nowpage != 1):
        mydict['showye'] = 1
    else:
        mydict['showye'] = 0

    showdict=[]
    page_list=[]
    start=(nowpage-1)*pageoffset+1

    if(start>len(data)):
        nowpage=total
    start=(nowpage-1)*pageoffset+1
    end = start + pageoffset - 1

    if (end > len(data)):
            end = len(data)

    i = start - 1
    while (i < end):
        showdict.append(data[i])
        i += 1

    pagestart = nowpage-2
    if(pagestart<=0):
        pagestart=1
    pageend = pagestart + maxshow -1
    if(pageend>total):
        pageend=total
        pagestart=total-maxshow+1
    if (pagestart <= 0):
        pagestart = 1

    i = pagestart
    while (i <= pageend):
            page_list.append(i)
            i += 1

    mydict['page_list'] = page_list
    mydict['showdict'] = showdict

    return mydict


def upinteger(a,b):
    result=a/b
    if(result>int(result)):
        result=int(result)+1
    result=int(result)
    return result

def getstartmonth(month):
    result={}
    year=9999999
    minmonth=13
    for i in month:
        array=i.split('.')
        if int(array[0])<year:
            year=int(array[0])
    for i in month:
        array=i.split('.')
        if(int(array[0])==year):
            if(int(array[1])<minmonth):
                minmonth=int(array[1])
    minmonth-=1
    return str(year)+','+str(minmonth)+',1'


