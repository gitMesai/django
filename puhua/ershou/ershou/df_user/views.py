#coding=utf-8
from django.shortcuts import render,redirect
from df_goods.models import GoodsInfo,TypeInfo
from df_order.models import OrderInfo
from . import user_decorator
from hashlib import sha1
from django.http import JsonResponse,HttpResponseRedirect,HttpResponse
from django.core.paginator import Paginator,Page
from df_user.models import UserInfo
import time


def register(request):
    context={'title':'大学生二手交易'}
    return render(request,'df_user/register.html',context)

#接收用户输入
def register_handle(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("cpwd")
        uemail = request.POST.get("email")
        if password != password2:
            return redirect('/user/register/')
        # 密码加密
        s1 = sha1()
        s1.update(password.encode('utf8'))
        password3 = s1.hexdigest()
        # 创建对象
        twz = UserInfo.objects.create(uname=username, upwd=password3,uemail=uemail)
        twz.save()
        # 注册成功，转到登陆页面
        return redirect('/user/login/')

#判断是否是已经有用（注册存在的功能）
def register_exist(request):
	#对应的是ajax请求
	uname = request.GET.get('uname')
	count = UserInfo.objects.filter(uname=uname).count()
	return JsonResponse({'count':count})#返回一个字典

#登陆
def login(request):
	uname = request.COOKIES.get('uname','')
	context={'title':'大学生二手交易','error_name':0,'error_pwd':0,'uname':uname}
	return render(request,'df_user/login.html',context)

def login_handle(request):
    #接收请求信息
    post=request.POST
    uname=post.get('username')
    upwd=post.get('pwd')
    jizhu=post.get('jizhu',0)
    #根据用户名查询对象
    users=UserInfo.objects.filter(uname=uname)#[]
    print (uname)
    #判断：如果未查到则用户名错，如果查到则判断密码是否正确，正确则转到用户中心
    if len(users)==1:
        s1=sha1()
        s1.update(upwd.encode('utf-8'))
        if s1.hexdigest()==users[0].upwd:
            url=request.COOKIES.get('url','/user/info/')
            red = HttpResponseRedirect(url)
            #记住用户名写入cookie
            if jizhu!=0:
                red.set_cookie('uname',uname)
            else:
                red.set_cookie('uname','',max_age=-1)#max_age是过期时间
            request.session['user_id']=users[0].id
            request.session['user_name']=uname
            return red
        else:
            context = {'title': '用户登录','error_name': 0,'error_pwd': 1,'uname':uname,'upwd':upwd}
            return render(request,'df_user/login.html',context)
    else:
        context = {'title': '用户登录','error_name':1,'error_pwd': 0,'uname':uname,'upwd':upwd}
        return render(request,'df_user/login.html',context)


def logout(request):
	request.session.flush()
	return redirect('/')

#用户信息
@user_decorator.login
def info(request):
	user_email=UserInfo.objects.get(id=request.session['user_id']).uemail
	#最近浏览
	goods_ids=request.COOKIES.get('goods_ids','')
	goods_ids1=goods_ids.split(',')

	goods_list=[]
	if goods_ids1[0]!='':
		for goods_id in goods_ids1:
			goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))

	context={'title':'天天生鲜用户中心',
			 'user_email':user_email,
			  'user_name':request.session['user_name'],
			   'goods_list':goods_list}
	return render(request,'df_user/user_center_info.html',context)

@user_decorator.login
def order(request,pindex):
	order_list=OrderInfo.objects.filter(user_id=request.session['user_id']).order_by('-oid')
	paginator=Paginator(order_list,2)
	if pindex=='':
		pindex='1'
	page=paginator.page(int(pindex))

	context={'title':'大学生二手交易',
			 'paginator':paginator,
			 'page':page,}
	return render(request,'df_user/user_center_order.html',context)

@user_decorator.login
def site(request):
	user = UserInfo.objects.get(id=request.session['user_id'])
	if request.method=='POST':
		post=request.POST
		user.ushouuser=post.get('ushou')
		user.uaddress=post.get('uaddress')
		user.uyoubian=post.get('uyoubian')
		user.uphone=post.get('uphone')
		user.save()
	context={'title':'大学生二手交易','user':user,}
	return render(request,'df_user/user_center_site.html',context)

@user_decorator.login
def publish(request):
    if request.method == 'POST':
        post=request.POST
        g_gtitle=post.get("gtitle")
        g_ttitle=post.get("ttitle")
        g_gpic=post.get("gpic")
        g_gjianjie=post.get("gjianjie")
        g_gkucun=post.get("gkucun")
        g_gprice=post.get("gprice")
        goods = GoodsInfo.objects.create(gtitle=g_gtitle,gpic=g_gpic,gjianjie=g_gjianjie,gkucun=g_gkucun,
                                         gprice=g_gprice,gtype_id=g_ttitle)
        goods.save()
        return redirect('/user/ginfo/')
    context = {'title': '大学生二手交易',}
    return render(request,'df_user/user_center_publish.html',context)

@user_decorator.login
def ginfo(request):
    context = {'title': '大学生二手交易',}
    return render(request,'df_user/user_center_ginfo.html',context)
