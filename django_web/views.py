# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decimal import *
from django.shortcuts import render, redirect, HttpResponse
from django_web.models import user,usewater,waterinfo,bill,employer
from functools import wraps
import json
from django.core.paginator import Paginator
import datetime
from django.contrib import messages
# 说明：这个装饰器的作用，就是在每个视图函数被调用时，都验证下有没法有登录，
# 如果有过登录，则可以执行新的视图函数，
# 否则没有登录则自动跳转到登录页面。
def check_login(f):
    @wraps(f)
    def inner(request,*arg,**kwargs):
        if request.session.get('is_login')=='1':
            return f(request,*arg,**kwargs)
        else:
            return redirect('/login/')
    return inner

def songshu(request):
    username = request.session.get('user_id')
    a = ""
    use = employer.objects.filter(eid=username)
    if use:
        request.session['is_login'] = '1'  # 这个session是用于后面访问每个页面（即调用每个视图函数时要用到，即判断是否已经登录，用此判断）
        # request.session['username']=username  # 这个要存储的session是用于后面，每个页面上要显示出来，登录状态的用户名用。
        # 说明：如果需要在页面上显示出来的用户信息太多（有时还有积分，姓名，年龄等信息），所以我们可以只用session保存user_id
        request.session['user_id'] = use[0].eid
        s = bill.objects.filter(eid_id=username)
        print (s)
        name = employer.objects.values('ename').get(eid=username)['ename']
        sex = employer.objects.values('esex').get(eid=username)['esex']
        phone = employer.objects.values('ephone').get(eid=username)['ephone']
        list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in s:
            st = int(i.num_id[4:6])
            list[st - 1] +=1
        print ('yes')
        return render(request, 'songshui.html',{'name':name,'id':username,'sex':sex,'phone':phone,'qiaozhi':list,'count':len(s)})
    else :
        a = '用户名或密码错误'
        # 如果是GET请求，就说明是用户刚开始登录，使用URL直接进入登录页面的
    return render(request, 'login.html', {'error_msg': a})

def songshui(request,username):
    a = ""
    use = employer.objects.filter(eid=username)
    if use:
        request.session['is_login'] = '1'  # 这个session是用于后面访问每个页面（即调用每个视图函数时要用到，即判断是否已经登录，用此判断）
        # request.session['username']=username  # 这个要存储的session是用于后面，每个页面上要显示出来，登录状态的用户名用。
        # 说明：如果需要在页面上显示出来的用户信息太多（有时还有积分，姓名，年龄等信息），所以我们可以只用session保存user_id
        request.session['user_id'] = use[0].eid
        s = bill.objects.filter(eid_id=username)
        print (s)
        name = employer.objects.values('ename').get(eid=username)['ename']
        sex = employer.objects.values('esex').get(eid=username)['esex']
        phone = employer.objects.values('ephone').get(eid=username)['ephone']
        list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in s:
            st = int(i.num_id[4:6])
            list[st - 1] +=1
        print ('yes')
        return render(request, 'songshui.html',{'name':name,'id':username,'sex':sex,'phone':phone,'qiaozhi':list,'count':len(s)})
    else :
        a = '用户名或密码错误'
        # 如果是GET请求，就说明是用户刚开始登录，使用URL直接进入登录页面的
    return render(request, 'login.html', {'error_msg': a})
def login(request):
    a = ""
    # 如果是POST请求，则说明是点击登录按扭 FORM表单跳转到此的，那么就要验证密码，并进行保存session
    if request.method=="POST":
        username=request.POST.get('name')
        password=request.POST.get('password')

        use=user.objects.filter(id=username,password=password)
        if use :
            print(username)
            print(password)
            print(use)
            if use:
                #登录成功
                # 1，生成特殊字符串
                # 2，这个字符串当成key，此key在数据库的session表（在数据库存中一个表名是session的表）中对应一个value
                # 3，在响应中,用cookies保存这个key ,(即向浏览器写一个cookie,此cookies的值即是这个key特殊字符）
                request.session['is_login']='1'  # 这个session是用于后面访问每个页面（即调用每个视图函数时要用到，即判断是否已经登录，用此判断）
                #request.session['username']=username  # 这个要存储的session是用于后面，每个页面上要显示出来，登录状态的用户名用。
                # 说明：如果需要在页面上显示出来的用户信息太多（有时还有积分，姓名，年龄等信息），所以我们可以只用session保存user_id
                request.session['user_id']=use[0].id
                s = usewater.objects.filter(id_id=username)
                name = user.objects.values('username').get(id=username)
                money = user.objects.values('balance').get(id=username)
                email = user.objects.values('email').get(id=username)
                print(s)
                list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                for i in s:
                    print (i.umonth[4:6])
                    list[int(i.umonth[4:6]) - 1] += float(i.ymoney)
                print (list)
                return render(request,'index.html',{'qiaozhi':list,'id':username,'name':name['username'],'money':sum(list),'count':len(s),'email':email['email'],'balance':money['balance']})
        else:
            return (songshui(request, username))
    return render(request, 'login.html')
    # 如果是GET请求，就说明是用户刚开始登录，使用URL直接进入登录页面的

def index(request):
    # students=Students.objects.all()  ## 说明，objects.all()返回的是二维表，即一个列表，里面包含多个元组
    # return render(request,'index.html',{"students_list":students})
    # username1=request.session.get('username')
    user_id1 = request.session.get('user_id')
    userobj = user.objects.filter(id=user_id1)
    password = user.objects.values('password').get(id=user_id1)
    email = user.objects.values('email').get(id=user_id1)
    # 使用user_id去数据库中找到对应的user信息
    if userobj:
        name = user.objects.values('username').get(id=user_id1)
        money = user.objects.values('balance').get(id=user_id1)
        s = usewater.objects.filter(id_id=user_id1)
        print(s)
        list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in s:
            print (i.umonth[4:6])
            list[int(i.umonth[4:6]) - 1] += float(i.ymoney)
        print (list)
        return render(request, 'index.html',
                      {'qiaozhi': list, 'id': user_id1, 'name': name['username'], 'money': sum(list),
                       'count': len(s),'balance':money['balance'],'password':password['password'],'email':email['email']})
    else:
        return render(request,'index.html',{'user','匿名用户'})


def register(request):
    check=''
    if request.method=='POST':
        id=request.POST.get("id")
        name = request.POST.get("name")
        password = request.POST.get("password")
        email = request.POST.get("email")
        use = user.objects.filter(id=id)
        if not use:
            user.objects.create(id=id,username=name,password=password,email=email)
            print('yes')
            return render(request, 'login.html')
        else:
            check='用户名已被占用'
    return render(request,'register.html',{'chec':check})
def xiugai(request):
    str = ''
    if request.method=='POST':
        id=request.POST.get("id")
        password = request.POST.get("password")
        repassword = request.POST.get("repassword")
        if password!=repassword:
            str='两次输入密码不同'
        else :
            use = user.objects.filter(id=id)
            if use:
                user.objects.filter(id=id).update(password=password)
            else:
                use = employer.objects.filter(eid=id)
                if use:
                    employer.objects.filter(eid=id).update(ekey=password)
                else:
                    str = '不存在此用户'
                    return render(request,'xiugaipassword.html',{'str':str})
            return redirect('/login/')
    return render(request,'xiugaipassword.html',{'str':str})
def table(request):
    years = []
    years = range(201800, 201813)
    years[0] = '全部'
    return render(request, 'table.html', {"data": years})

def jiedan(request):
    years = []
    years = range(201800, 201813)
    years[0] = '全部'
    return render(request, 'jiedan.html', {"data": years})

def jiedan2(request):
    years = []
    years = range(201800, 201813)
    years[0] = '全部'
    return render(request, 'jiedan2.html', {"data": years})

def get_watername (a):
    use = waterinfo.objects.values('wname').get(wid=a)
    return use['wname']

def get_smoney(a):
    use = bill.objects.values('smoney').filter(num_id=a)
    if use:
        use = bill.objects.values('smoney').get(num_id=a)
        return use['smoney']
    else:
        return '0.00'

def getnames(id):
    use = user.objects.values('username').filter(id=id)
    if use:
        use = user.objects.values('username').get(id=id)
        return use['username']
    else:
        return use
def getadd(name):
    use = user.objects.values('email').filter(id=name)
    if use:
        use = user.objects.values('email').get(id=name)
        return use['email']
    else:
        return use
def show_asset_in_table2(request):
    if request.method == "GET":
        limit = request.GET.get('limit')  # how many items per page
        offset = request.GET.get('offset')  # how many items in total in the DB
        sort_column = request.GET.get('sort')  # which column need to sort
        order = request.GET.get('order')
        asset_id = request.GET.get('qiao')
        riqi = request.GET.get('zhi')
        print (asset_id)
        print (riqi)
        # ascending or descending
        if (not asset_id and riqi=='全部'):
            all_records = usewater.objects.filter(flag2=0)
        elif (asset_id and riqi=='全部'):
            all_records = usewater.objects.filter(num=asset_id,flag2=0)
        elif (not asset_id and riqi!='全部'):
            all_records = usewater.objects.filter(umonth=riqi,flag2=0)
        else:
            all_records = usewater.objects.filter(umonth=riqi,num=asset_id,flag2=0)

        print (all_records)
        if sort_column:  # 判断是否有排序需求
            sort_column = sort_column.replace('asset_', '')
            if sort_column in ['asset_id', 'asset_riqi']:  # 如果排序的列表在这些内容里面
                if order == 'desc':  # 如果排序是反向
                    sort_column = '-%s' % (sort_column)
                all_records = usewater.objects.all().order_by(sort_column)


                #     annotate 是注释的功能,localdisks_size前端传过来的是这个值，后端也必须这样写，Sum方法是django里面的，不是小写的sum方法，
                # 两者的区别需要注意，Sum（'disk__capacity‘）表示对disk表下面的capacity进行加法计算，返回一个总值.
        all_records_count = all_records.count()

        if not offset:
            offset = 0
        if not limit:
            limit = 20  # 默认是每页20行的内容，与前端默认行数一致
        pageinator = Paginator(all_records, limit)  # 开始做分页

        page = int(int(offset) / int(limit) + 1)
        response_data = {'total': all_records_count, 'rows': []}  # 必须带有rows和total这2个key，total表示总页数，rows表示每行的内容

        for asset in pageinator.page(page):# 获取磁盘和内存的大小
            # 下面这些asset_开头的key，都是我们在前端定义好了的，前后端必须一致，前端才能接受到数据并且请求.
            response_data['rows'].append({
                "asset_id": asset.num,
                "asset_name": getnames(asset.id_id) if getnames(asset.id_id) else "",
                "asset_riqi": asset.umonth if asset.umonth else "",
                "asset_water_c": asset.water_c if asset.water_c else "",
                "asset_water_id": asset.wid_id if asset.wid_id else "",
                "asset_water_flag": get_watername(asset.wid_id)if get_watername(asset.wid_id) else "",
                "asset_ymoney": str(asset.ymoney) if asset.ymoney else "",
                "asset_add": getadd(asset.id_id) if getadd(asset.id_id) else "",
            })
            print (response_data)
        return HttpResponse(json.dumps(response_data))

def show_asset_in_table3(request):
    if request.method == "GET":
        user_id1 = request.session.get('user_id')
        print (user_id1)
        print(request.GET)
        print (id)
        limit = request.GET.get('limit')  # how many items per page
        offset = request.GET.get('offset')  # how many items in total in the DB
        sort_column = request.GET.get('sort')  # which column need to sort
        order = request.GET.get('order')
        asset_id = request.GET.get('qiao')
        riqi = request.GET.get('zhi')
        print (asset_id)
        print (riqi)
        # ascending or descending
        all_records = []
        s = bill.objects.filter(eid=user_id1)
        print (s)
        j =0
        if (not asset_id and riqi=='全部'):
            for i in s:
                if usewater.objects.filter(num=i.num_id,flag2=1):
                    all_records.append(usewater.objects.get(num=i.num_id,flag2=1))
                    j+=1
        elif (asset_id and riqi=='全部'):
            for i in s:
                if asset_id in i:
                    if usewater.objects.filter(num=i.num_id,flag2=1):
                        all_records.append(usewater.objects.get(num=i.num_id,flag2=1))
                        j += 1
        elif (not asset_id and riqi!='全部'):
            for i in s:
                if usewater.objects.filter(umonth=riqi,num=i.num_id,flag2=1):
                    all_records.append(usewater.objects.get(umonth=riqi,num=i.num_id,flag2=1))
                    j += 1
        else:
            for i in s:
                if usewater.objects.filter(umonth=riqi,num=i.num_id,flag2=1):
                    all_records.append(usewater.objects.get(umonth=riqi,num=i.num_id,flag2=1))
                    j += 1

        print (all_records)
        if sort_column:  # 判断是否有排序需求
            sort_column = sort_column.replace('asset_', '')
            if sort_column in ['asset_id', 'asset_riqi']:  # 如果排序的列表在这些内容里面
                if order == 'desc':  # 如果排序是反向
                    sort_column = '-%s' % (sort_column)
                all_records = usewater.objects.all().order_by(sort_column)

        all_records_count = j
        print (j)
        if not offset:
            offset = 0
        if not limit:
            limit = 20  # 默认是每页20行的内容，与前端默认行数一致
        pageinator = Paginator(all_records, limit)  # 开始做分页

        page = int(int(offset) / int(limit) + 1)
        response_data = {'total': all_records_count, 'rows': []}  # 必须带有rows和total这2个key，total表示总页数，rows表示每行的内容

        for asset in pageinator.page(page):# 获取磁盘和内存的大小
            # 下面这些asset_开头的key，都是我们在前端定义好了的，前后端必须一致，前端才能接受到数据并且请求.
            response_data['rows'].append({
                "asset_id": asset.num,
                "asset_name": getnames(asset.id_id) if getnames(asset.id_id) else "",
                "asset_riqi": asset.umonth if asset.umonth else "",
                "asset_water_c": asset.water_c if asset.water_c else "",
                "asset_water_id": asset.wid_id if asset.wid_id else "",
                "asset_water_flag": get_watername(asset.wid_id)if get_watername(asset.wid_id) else "",
                "asset_ymoney": str(asset.ymoney) if asset.ymoney else "",
                "asset_add": getadd(asset.id_id) if getadd(asset.id_id) else "",
            })
            print (response_data)
        return HttpResponse(json.dumps(response_data))

def geteid(num):
    if bill.objects.filter(num_id=num):
        return bill.objects.values('eid_id').get(num_id=num)['eid_id']
    else:
        return bill.objects.filter(num_id=num)

def getename(num):
    if bill.objects.filter(num_id=num):
        s = bill.objects.values('eid_id').get(num_id=num)['eid_id']
        return employer.objects.values('ename').get(eid=s)['ename']
    else:
        return bill.objects.filter(num_id=num)

def show_asset_in_table(request):
    '''
    专门处理在服务器资产列表里面的表格信息的方法
    :param request:
    :return:
    '''
    if request.method == "GET":
        print(request.GET)
        id = request.session.get('user_id')
        print (id)
        limit = request.GET.get('limit')  # how many items per page
        offset = request.GET.get('offset')  # how many items in total in the DB
        sort_column = request.GET.get('sort')  # which column need to sort
        order = request.GET.get('order')
        asset_id = request.GET.get('qiao')
        riqi = request.GET.get('zhi')
        print (asset_id)
        print (riqi)
        # ascending or descending
        if (not asset_id and riqi=='全部'):
            all_records = usewater.objects.filter(id_id=id)
        elif (asset_id and riqi=='全部'):
            all_records = usewater.objects.filter(num=asset_id,id_id=id)
        elif (not asset_id and riqi!='全部'):
            all_records = usewater.objects.filter(umonth=riqi,id_id=id)
        else:
            all_records = usewater.objects.filter(umonth=riqi,num=asset_id,id_id=id)

        print (all_records)
        if sort_column:  # 判断是否有排序需求
            sort_column = sort_column.replace('asset_', '')
            if sort_column in ['asset_id', 'asset_riqi']:  # 如果排序的列表在这些内容里面
                if order == 'desc':  # 如果排序是反向
                    sort_column = '-%s' % (sort_column)
                all_records = usewater.objects.all().order_by(sort_column)


                #     annotate 是注释的功能,localdisks_size前端传过来的是这个值，后端也必须这样写，Sum方法是django里面的，不是小写的sum方法，
                # 两者的区别需要注意，Sum（'disk__capacity‘）表示对disk表下面的capacity进行加法计算，返回一个总值.
        all_records_count = all_records.count()

        if not offset:
            offset = 0
        if not limit:
            limit = 20  # 默认是每页20行的内容，与前端默认行数一致
        pageinator = Paginator(all_records, limit)  # 开始做分页

        page = int(int(offset) / int(limit) + 1)
        response_data = {'total': all_records_count, 'rows': []}  # 必须带有rows和total这2个key，total表示总页数，rows表示每行的内容

        for asset in pageinator.page(page):# 获取磁盘和内存的大小
            # 下面这些asset_开头的key，都是我们在前端定义好了的，前后端必须一致，前端才能接受到数据并且请求.
            response_data['rows'].append({
                "asset_id": asset.num,
                "asset_riqi": asset.umonth if asset.umonth else "",
                "asset_flag": asset.flag if asset.flag else "",
                "asset_water_c": asset.water_c if asset.water_c else "",
                "asset_water_id": asset.wid_id if asset.wid_id else "",
                "asset_water_flag": get_watername(asset.wid_id)if get_watername(asset.wid_id) else "",
                "asset_ymoney": str(asset.ymoney) if asset.ymoney else "",
                "asset_eid":geteid(asset.num) if geteid(asset.num) else "目前还未被接单",
                "asset_ename":getename(asset.num) if getename(asset.num) else "目前还未被接单",
            })
            print (response_data)
        return HttpResponse(json.dumps(response_data))  # 需要json处理下数据格式
def dingdan (request):
    nid = request.session.get('user_id')
    print ('1231321131313231')
    print (nid)
    name = user.objects.values('username').get(id=nid)
    all_records = waterinfo.objects.all()
    list1 = []
    list2 = []
    for i in all_records:
        list1.append(i.wname)
        list2.append(i.price)
        print ("yes")
    return render(request, 'dingdan.html',{'list1':list1[0],'list2':list1[1],'list3':list1[2],'list4':list1[3],'list5':list1[4],'list6':list1[5],'list11':list2[0],'list12':list2[1],'list13':list2[2],'list14':list2[3],'list15':list2[4],'list16':list2[5],'name':name['username'],'id':nid})

def findwid (name):
    qiao = waterinfo.objects.values('wid').get(wname=name)
    print (qiao['wid'])
    return qiao['wid']

def getcount(id):
    balance = user.objects.values('balance').get(id=id)
    print (balance)
    return balance['balance']

def zhifu(request):
    if request.method=='POST':
        number = []
        name = []
        qiaozhi=0
        print (int(request.POST.get('itemss')))
        for i in range(1, int(request.POST.get('itemss')) + 1):
            qiaozhi = qiaozhi+float(request.POST.get('amount_'+str(i)))
        if (getcount(request.session.get('user_id'))>=qiaozhi):
            qiaozhi=0
            i=1
            for i in range(1,int(request.POST.get('itemss'))+1):
                a = request.POST.get('quantity_'+str(i))
                b = request.POST.get('amount_'+str(i))
                c = request.POST.get('w3ls_item_'+str(i))
                print (c)
                wid =findwid(c)
                e = datetime.datetime.now().strftime('%Y%m%d')
                w = datetime.datetime.now().strftime('%Y%m')
                d = usewater.objects.values('num').filter(umonth=w)
                g=0
                if d:
                    for j in d:
                        zhi = j['num'][8:]
                        f1 = int (zhi)
                        if (f1>g):
                            g = int(f1)
                    s = e+str(g+1)
                else:
                    s = e+str(qiaozhi+1)
                usewater.objects.create(num=s,umonth=w,water_c=a,ymoney=float(b)*float(a),id_id=request.session.get('user_id'),wid_id=wid)
                print ('YES')
            return render(request, 'dingdan/zhifu.html',{'name':2})
        else:
            return render(request, 'dingdan/zhifu.html',{'name':1})
    else:
        return render(request, 'dingdan/zhifu.html',{'name':3})

def a(request):
    s = request.session.get('user_id')
    data = json.loads(request.body)
    print (data["name"])
    if (data["id"]=='1'):
        user.objects.filter(id=s).update(username=data["name"])
    elif (data["id"] == '2'):
        w = user.objects.values('balance').get(id=s)
        print (Decimal.from_float(float(data["name"]))+w['balance'])
        user.objects.filter(id=s).update(balance=Decimal.from_float(float(data["name"]))+w['balance'])
    elif (data["id"] == '4'):
        user.objects.filter(id=s).update(email=data["name"])
    else:
        dict = {
            "status": 0,
        }
        ret = json.dumps(dict)
        return HttpResponse(ret)
    dict = {
        "status":1,
    }
    ret = json.dumps(dict)
    return HttpResponse(ret)

def b (request):
    data = json.loads(request.body)
    id = data["id"]
    print (id)
    for i in id:
        usewater.objects.filter(num=i).update(flag="已达")
    dict = {
        "status": 1,
    }
    print ('yes')
    ret = json.dumps(dict)
    return HttpResponse(ret)

def c (request):
    s = request.session.get('user_id')
    data = json.loads(request.body)
    id = data["id"]
    print (id)
    for i in id:
        print ('yes')
        usewater.objects.filter(num=i).update(flag2=1)
        bill.objects.create(num_id=i,eid_id=s)
    dict = {
        "status": 1,
    }
    ret = json.dumps(dict)
    return HttpResponse(ret)

def d(request):
    s = request.session.get('user_id')
    data = json.loads(request.body)
    print (data["name"])
    if (data["id"]=='1'):
        employer.objects.filter(eid=s).update(ename=data["name"])
    elif (data["id"] == '2'):
        employer.objects.filter(eid=s).update(esex=data["name"])
    elif (data["id"] == '4'):
        employer.objects.filter(eid=s).update(ephone=data["name"])
    else:
        dict = {
            "status": 0,
        }
        ret = json.dumps(dict)
        return HttpResponse(ret)
    dict = {
        "status":1,
    }
    ret = json.dumps(dict)
    return HttpResponse(ret)

def employerregister(request):
    check = ''
    if request.method == 'POST':
        id = request.POST.get("id")
        name = request.POST.get("name")
        password = request.POST.get("password")
        phone = request.POST.get("phone")
        sex = request.POST.get("sex")
        use = bill.objects.filter(eid=id)
        if not use:
            employer.objects.create(eid=id, ename=name, ekey=password,ephone=phone,esex=sex)
            print('yes')
            return render(request, 'login.html')
        else:
            check = '用户名已被占用'
    return render(request, 'employerregister.html', {'chec': check})

def e(request):
    return render(request, 'login.html')
