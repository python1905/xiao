import hashlib
import os

from django.contrib.auth import logout
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.crypto import random
from App.file import check_file_type, check_file_size

from App.verification_code import send_sms

from django.urls import reverse

from App.forms import UserForm, PW, UserName
from App.models import User, Paymenu, List, Index, Detail, Cart, Settlement
from xiaomi.settings import maxage, MEDIA_ROOT


from alipay import AliPay
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
# Create your views here.
from rest_framework.response import Response

from xiaomi.settings import ALI_APP_ID, APP_PRIVATE_KEY, ALIPAY_PUBLIC_KEY


# 登录页面
def login(request):
    return render(request, 'app/login.html')


# 验证用户登录
def verify_login(request):
    user = request.POST.get('user')
    password = request.POST.get('password')
    password1 = hashlib.sha1(password.encode()).hexdigest()
    print(password1)
    # 查询出数据库是否有这个用户名  返回的就是一个的字典
    user1 = User.objects.values('password', 'username', 'portrait', 'cellphone').filter(
        Q(cellphone=user) | Q(xiaomiid=user)).first()
    # print(user1, type(user1))
    # print(user1['password'])

    if user1:
        if user1['password'] == password1:
            # 将手机号写入session用于判断用户是否登录
            request.session['user'] = user1['cellphone']
            # 将页面展示的信息从数据库取出来
            username = user1['username']
            photo = user1['portrait']
            return render(request, 'app/index.html', {'username': username, 'photo': photo})

    return render(request, 'app/login.html', {'error': '·  密码或用户名错误'})


# 退出登录
# def loginout(request):
#     logout()
#     return render(request, 'app/index')


# 用户注册
def user_enroll(request):
    if request.method == 'POST':
        print("post")
        # 获取提交的表单类
        form = UserForm(request.POST)
        if form.is_valid():
            print("a")
            # 获取电话号码
            p = request.POST.get('phone')
            # 随机生成验证码
            a = str()
            for i in range(5):
                num = str(random.randint(0, 9))
                a = a + num

            # 向用户发送验证码
            # send_sms(p, {'number': a})
            # 将验证码写入session
            request.session['yzm'] = a
            request.session['phone'] = p
            f = request.session.get('yzm')
            print(f)
            # 设置过期时间
            request.session.set_expiry(maxage)

            b = 1
            return render(request, 'app/enroll.html', {'a': b, 'phone': p})

        return render(request, 'app/enroll.html', {'form': form})
    return render(request, 'app/enroll.html')


# 判断验证码
def is_sms(request):
    phone = request.session.get('phone')
    # 获取提交的验证码
    sms = request.POST.get('ticket')
    # print(sms, type(sms))
    yzm = request.session.get('yzm')
    if sms == yzm:
        c = 2
        return render(request, 'app/enroll.html', {'c1': c, 'phone': phone})

    else:
        b = 1
        return render(request, 'app/enroll.html', {'a': b, 'error': '验证码错误或以过期'})


# 保存密码
def password(request):
    form1 = PW(request.POST)
    if form1.is_valid():
        # 将手机号存入数据库
        phone = request.session.get('phone')
        # User.objects.create(cellphone=p)
        #
        # 删除多余的repassword
        # del form1.cleaned_data['repassword']
        # 保存到数据库密码
        p = request.POST.get('password')
        p1 = hashlib.sha1(p.encode()).hexdigest()
        # 保存小米id
        xiaomiid = str()
        for i in range(10):
            num = str(random.randint(0, 9))
            xiaomiid = xiaomiid + num

        User.objects.create(cellphone=phone, password=p1, xiaomiid=xiaomiid)
        # User.objects.create(**form1.cleaned_data)

        win = 'yes'
        return render(request, 'app/enroll.html', {'win': win, 'xiaomiid': xiaomiid})

    c = 2
    return render(request, 'app/enroll.html', {'c1': c, 'form1': form1})


# 头像设置
def user(request):
    photo = User.objects.values('portrait', 'xiaomiid', 'username').filter(cellphone='13754834137').first()

    photo1 = photo['portrait']
    xiaomiid = photo['xiaomiid']
    username = photo['username']

    if request.method == 'POST':
        # 获取文件上传对象
        file = request.FILES.get('file')
        # 文件上传检测
        if not (check_file_size(file.size) and check_file_type(file.name)):
            return HttpResponse("文件大小或者类型不匹配")
        # 把上传文件的内容保存到当前用户中
        # 当前用户的手机号
        phone = request.session.get('phone')
        # 查出当前手机号的模型对象
        user = User.objects.filter(cellphone=phone).first()
        # user = User.objects.filter(cellphone='13754834137').first()
        print(user, type(user))
        user.portrait = file
        # 保存到数据库
        user.save()
        # 从数据库取出图片地址
        photo = User.objects.values('portrait', 'xiaomiid', 'username').filter(cellphone=phone).first()
        # photo = User.objects.values('portrait', 'xiaomiid', 'username').filter(cellphone='13754834137').first()
        print(photo, '1111')
        photo1 = photo['portrait']
        xiaomiid = photo['xiaomiid']
        username = photo['username']
        print(xiaomiid)
        print(photo)
        return render(request, 'app/user.html', {'photo': photo1, 'xiaomiid': xiaomiid, 'username': username})
        # return HttpResponse('成功')
    return render(request, 'app/user.html', {'photo': photo1, 'xiaomiid': xiaomiid, 'username': username})


# 用户名 性别设置
def user1(request):
    form2 = UserName(request.POST)
    if form2.is_valid():
        gender = request.POST.get('gender')
        username = request.POST.get('nickname')
        # 当前用户的手机号
        phone = request.session.get('phone')
        # 查出当前手机号的模型对象
        user = User.objects.filter(cellphone=phone).first()
        # user = User.objects.filter(cellphone='13754834137').first()
        # 修改username字段的内容
        user.username = username
        user.gender = gender
        # 保存数据库
        user.save()
        photo = User.objects.values('portrait', 'xiaomiid').filter(cellphone=phone).first()
        photo1 = photo['portrait']
        xiaomiid = photo['xiaomiid']
        gender1 = ""
        if gender == '0':
            gender1 = '男'
        elif gender == '1':
            gender1 = '女'
        return render(request, 'app/user.html',
                      {'username': username, 'gender': gender1, 'photo': photo1, 'xiaomiid': xiaomiid})

    return render(request, 'app/user.html', {'form2': form2})


def index(request):
    menus = Index.objects.all()
    title = Paymenu.objects.all()
    cellphone = request.session.get('user')
    if not cellphone:
        return render(request, "app/index.html", context={"menus": menus, 'title': title})
    else:
        user1 = User.objects.values('username', 'portrait').filter(cellphone=cellphone).first()

        username = user1['username']
        photo = user1['portrait']
        return render(request, "app/index.html", context={"menus": menus, 'title': title,
                                                          'username': username, 'photo': photo})


def search(request):
    if request.method == 'POST':
        canshu = request.POST.get('shousuo')
        list = Index.objects.all()
        return render(request, "app/search_list.html", {'canshu': canshu, 'lists': list})
    return HttpResponseRedirect('/index/')


def list(request):
    title = Paymenu.objects.all()
    list = List.objects.all()
    return render(request, 'app/list.html', {'titles': title, 'lists': list})


def detail(request):
    detail = Index.objects.all()
    image = Detail.objects.all()
    id = request.GET.get('id')
    parameter = int(id)
    return render(request, 'app/details.html', context={'details': detail, 'parameter_id': parameter, 'image': image})


def shopping_cart(request):
    commodity = Index.objects.all()
    title = request.GET.get('tit')
    for value in commodity:
        value_title = str(value.title)
        if title == value_title:
            cart_id = Cart.objects.filter(title=value.title)
            if not len(cart_id) == 0:  # 判断列表不为空
                cart = Cart.objects.get(title=value.title)
                cart.digital += 1
                cart.save()
            else:
                add_cart = Cart(image=value.image, title=value.title, price=value.price, total_price=value.price)
                add_cart.save()
    cart = Cart.objects.all()
    if len(cart) == 0:
        return render(request, 'app/shopping_null.html')
    return render(request, 'app/shopping_cart.html', {'commodity': cart, 'titles': title})


def delete(request):
    id = request.GET.get('id')
    cart = Cart.objects.filter(id=id)
    parameter = int(id)
    print(parameter)
    for cart_id in cart:
        print(cart_id.id)
        if parameter == cart_id.id:
            cart.delete()
        return HttpResponseRedirect('/app/')


def settlement(request):
    sett = Cart.objects.all()
    title = request.GET.get('tit')
    print(title)
    for value in sett:
        value_title = str(value.title)
        if title == value_title:
            sett_id = Settlement.objects.filter(title=value.title)
            if not len(sett_id) == 0:  # 判断列表不为空
                sett = Settlement.objects.get(title=value.title)
                sett.quantity += 1
                sett.save()
            else:
                add_cart = Settlement(image=value.image, title=value.title, price=value.price)
                add_cart.save()
    settle = Settlement.objects.all()
    return render(request, 'app/settlement.html', {'settles': settle, 'titles': title})


@api_view(["GET", "POST"])
def ali_buy(request):
    order_no = "2019082102983"

    alipay = AliPay(
        appid=ALI_APP_ID,
        app_notify_url=None,  # 默认回调url
        app_private_key_string=APP_PRIVATE_KEY,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=ALIPAY_PUBLIC_KEY,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=False  # 默认False
    )

    order_string = alipay.api_alipay_trade_wap_pay(
        out_trade_no="2019061900100",
        total_amount=30,
        subject="macpro",
        return_url="http://localhost:8000/cart/index",
        notify_url="http://localhost:8000/cart/index"  # 可选, 不填则使用默认notify url
    )

    # 支付宝网关
    net = "https://openapi.alipaydev.com/gateway.do"

    data = {
        "msg": "ok",
        "status": 200,
        "data": {
            "pay_url": net + order_string
        }
    }

    return Response(data)