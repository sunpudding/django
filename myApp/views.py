# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import forms
from .models import Users,Messages
import datetime
import json

class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=30)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())

class ChangeForm(forms.Form):
    username = forms.CharField(label='用户名')
    old_password = forms.CharField(label='原密码',widget=forms.PasswordInput())
    new_password = forms.CharField(label='新密码',widget=forms.PasswordInput())

def mes(request):
    """用户在登录状态

    返回该用户所创建的留言"""
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        username = request.session.get('USRNAME', False)
        response = HttpResponseRedirect('/login/',)
        # 将username写入浏览器cookie,失效时间为3600
        response.set_cookie('username', username, 3600)
        p =Users.objects.filter(username=username)
        messages_list = Messages.objects.filter(username=username)
        # 生成paginator对象,定义每页显示10条记录
        paginator = Paginator(messages_list,10 )

        # 从前端获取当前的页码数,默认为1
        page = request.GET.get('page', 1)
        try:
            messages_list = paginator.page(int(page))  # 获取当前页码的记录
        except PageNotAnInteger:
            messages_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
        except EmptyPage:
            messages_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
        return render(request, 'myApp/mes.html', locals(),{"username":username,'messages_list': messages_list})

    else:
        return HttpResponse('用户名或密码错误,请重新登录')

def index(request):
    """获取所有留言内容


    返回主页，将所有留言显示在主页上"""
    messages_list =Messages.objects.all()

    # 生成paginator对象,定义每页显示20条记录
    paginator = Paginator(messages_list, 20)

    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)

    # 把当前的页码数转换成整数类型
    currentPage = int(page)

    try:
        print(page)
        messages_list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        messages_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        messages_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    return render(request,'myApp/start.html',locals())

def login(request):
    """创建用户登录


    返回登录的页面"""
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']
            request.session['IS_LOGIN'] = True
            request.session['USRNAME'] = username
            response = HttpResponseRedirect('/login/')
            response.set_cookie('username', username, 3600)
            #user = Users.objects.filter(username__exact=username,password__exact=password)
            is_login = request.session.get('IS_LOGIN', False)
            if is_login:
                messages= Messages.objects.all()
                paginator = Paginator(messages, 15)
                page = request.GET.get('page', 1)
                currentPage = int(page)
                try:
                    # 尝试获取请求的页数的信息
                    Message = paginator.page(currentPage)
                    # 请求页数错误
                except PageNotAnInteger:
                    Message = paginator.page(1)
                except EmptyPage:
                    Message = paginator.page(paginator.num_pages)
                return render(request,'myApp/loginsuccess.html', {'Message': Message})
            else:
                return HttpResponse('用户名或密码错误,请重新登录')
    else:
        userform = UserForm()
    return render_to_response('myApp/login.html', {'userform': userform})


def regist(request):
    """注册用户的账户信息

    返回注册成功信息"""
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            #获取表单数据
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            #添加到数据库
            registAdd = Users.objects.get_or_create(username = username,password = password)[1]
            if registAdd == False:
                return render_to_response('myApp/registReturn.html',{'registAdd':registAdd,'username':username})
            else:
                return render_to_response('myApp/registReturn.html',{'registAdd':registAdd})
    else:
        uf = UserForm()
    return render_to_response('myApp/regist.html',{'uf':uf})

def logout(request):
    """注销用户的登录状态

    返回注销的结果"""
    try:
        del request.session['username'] # 将用户名从session中删除
    except KeyError:
        pass
    return render(request, 'myApp/logout.html')


def changepwd(request):
    """修改用户的密码

    返回修改后的结果"""
    if request.method == 'POST':
        uf = ChangeForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            old_password = uf.cleaned_data['old_password']
            new_password = uf.cleaned_data['new_password']

            ##判断用户原密码是否匹配
            user = Users.objects.filter(username=username)
            if user:
                passwd = Users.objects.filter(username=username, password=old_password)
                if passwd:
                    Users.objects.filter(username=username, password=old_password).update(
                        password=new_password)  ##如果用户名、原密码匹配则更新密码
                    info = '密码修改成功!'
                else:
                    info = '请检查原密码是否输入正确!'
            elif len(user) == 0:
                info = '请检查用户名是否正确!'

        return HttpResponse(info)
    else:
        uf = ChangeForm()
    return render_to_response('myApp/changepwd.html', {'uf': uf})


def createM(request):
    """在用户的登录状态，创建该用户的留言

    返回留言的页面，创建该用户的新留言"""
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        username = request.session.get('USRNAME', False)
        return render(request, 'myApp/createM.html',{"username":username})
    else:
        return redirect("myApp/login.html")

def saveM(request):
    """用户创建留言后，保存留言

    返回保存留言后的用户页面"""
    username = request.POST.get("username")
    title = request.POST.get("title")
    content = request.POST.get("content")
    publish = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    messageB = Messages(title=title, content=content, username=username, publish=publish)
    messageB.save()
    Message = Messages.objects.all()
    return render(request, 'myApp/loginsuccess.html',{"Message":Message})

def latest_msg(request):
    """创建留言后

    返回最近十分钟创建的留言"""
    now = datetime.datetime.now()
    start = now - datetime.timedelta(minutes=10)
    a = Messages.objects.filter(publish__gt=start)
    from django.core import serializers
    ms_json = serializers.serialize("json", a)
    return render(request, 'myApp/latest_msg.html', {'ms_json': json.dumps(ms_json)})

