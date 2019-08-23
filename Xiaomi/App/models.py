# from django.contrib.auth.hashers import make_password, check_password
import hashlib

from django.contrib.auth.hashers import make_password, check_password
from django.db import models

# Create your models here.
from django.http import request


class User(models.Model):
    uid = models.AutoField(primary_key=True)
    cellphone = models.CharField(max_length=11, unique=True)
    password = models.CharField(max_length=200)
    xiaomiid = models.CharField(max_length=200, null=True)
    orderformid = models.IntegerField(null=True)
    collectid = models.IntegerField(null=True)
    site = models.IntegerField(null=True)
    portrait = models.ImageField(upload_to='file', null=True)
    username = models.CharField(max_length=200, null=True)
    gender = models.IntegerField(default=0, choices=(('0', '女'), ('1', '男')), null=True)

    class Meta:
        managed = True
        db_table = 'mi_user'

    # @property
    # def password(self):
    #     # 把加密后的密码返回到数据库
    #     return self.password_hash
    #
    #
    # @password.setter
    # def password(self, value):
    #     self.password_hash = hashlib.sha1(value.encode('utf8')).hexdigest()


    # # 第一个参数是提交的密码   第二个参数是数据库的密码
    # def check_login(self,newpassword,database_password):
    #     # 验证密码是否相等 返回的布尔值
    #     return check_password(newpassword,database_password)

    # user=User()
    # password = request.POST.get('password')
    # if check_login(password,user.password):
    #     pass
    # else:


# Create your models here.
class Index(models.Model):
    id = models.AutoField(primary_key=True)
    menu = models.CharField(max_length=40)
    mid = models.IntegerField(null=True)
    pay_menu = models.CharField(max_length=20)
    image = models.CharField(max_length=100)
    big_title = models.CharField(max_length=10)
    pay_title = models.CharField(max_length=20)
    select = models.CharField(max_length=20,null=True)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=100)
    price = models.IntegerField(null=True)
    plate_id = models.IntegerField(null=True)
    product_description = models.CharField(max_length=100)
    big_image = models.CharField(max_length=100,null=True)

    class Meta:
        db_table = 'xiaomi_index'

class Paymenu(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.CharField(max_length=100)
    content = models.CharField(max_length=50)
    pid = models.ImageField(null=True)

    class Meta:
        db_table = 'xiaomi_paytitle'

class List(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.CharField(max_length=100)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=50)
    price = models.IntegerField(null=True)
    pid = models.IntegerField(null=True)

    class Meta:
        db_table = 'xiaomi_list'

class Detail(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.CharField(max_length=100)
    image_1 = models.CharField(max_length=100)
    image_2 = models.CharField(max_length=100)
    image_3 = models.CharField(max_length=100)
    image_4 = models.CharField(max_length=100)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    price = models.IntegerField(null=True)
    delivery = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    # overview = models.CharField(max_length=100)
    # comment = models.CharField(max_length=100)
    pid = models.IntegerField(null=True)

    class Meta:
        db_table = 'xiaomi_detail'

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.CharField(max_length=100)
    title = models.CharField(max_length=50)
    price = models.IntegerField()
    digital = models.IntegerField(default=1)
    total_price = models.IntegerField()

    class Meta:
        db_table = 'xiaomi_cart'

class Settlement(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.CharField(max_length=100)
    title = models.CharField(max_length=50)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table = 'xiaomi_settlement'