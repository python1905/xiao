

# 自定义表单
import re

from django import forms
from django.core.exceptions import ValidationError





class UserForm(forms.Form):
    # password = forms.CharField()
    phone = forms.CharField(min_length=11, max_length=11,
                            error_messages={
                                'required': '手机号必须输入',
                                'max_length': '手机号长度必须是11位',
                                'min_length': '手机号长度必须是11位'
                            })
    # 自定义验证字段
    # 方法名规则  clean_字段名
    def clean_phone(self):
        # 必须使用cleaned_data获取数据
        phone = self.cleaned_data.get('phone')
        if re.match(r'1[3,5,6,7,8,9]\d{9}$', phone):
            return phone
        raise ValidationError('手机格式错误！')

def check_password(password):
    if re.match(r'\d+$', password):
        raise ValidationError("密码不能是纯数字")

class PW(forms.Form):
    password = forms.CharField(min_length=3,
                               # widget=forms.PasswordInput(attrs={
                               #     'placehold':'请输入密码',
                               #     'class': 'passwoed'
                               # }),
                               error_messages={
                                   'required': '密码必须输入',
                                   'min_length': '密码不能少于8位'
                               },
                               validators = [check_password]
                               )
    repassword = forms.CharField(min_length=3,
                               # widget=forms.PasswordInput(attrs={
                               #     'placehold':'请输入密码',
                               #     'class': 'repasswoed'
                               # }),
                               error_messages={
                                   'required': '密码必须输入',
                                   'min_length': '密码不能少于6位'
                               },
                               validators = [check_password]
                                )



    def clean(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('repassword')
        if password1 == password2:
            return self.cleaned_data
        raise ValidationError({'repassword':'两次密码不一致'})


class UserName(forms.Form):

    nickname = forms.CharField(min_length=3, max_length=11,
                            error_messages={
                                'required': '姓名不能为空',
                                'max_length': '姓名必须是3-11位的数字',
                                'min_length': '姓名必须是3-11位的数字'
                            })
