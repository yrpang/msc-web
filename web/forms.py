from django import forms
from django.forms import formset_factory, ModelForm, modelformset_factory, widgets
from .models import Answers, Questions
import re
from django.core.exceptions import ValidationError


class UserForm(forms.Form):
    email = forms.EmailField(label="邮箱", max_length=128, widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))


class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    name = forms.CharField(label="姓名", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender,
                            widget=forms.Select(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    birth = forms.DateField(error_messages={'invalid': '出生日期格式错误 正确样例1999-01-01'}, label='出生日期', widget=forms.DateInput(
        format=('%d-%m-%Y'), attrs={'class': 'form-control', 'placeholder': '1999-01-01'}))
    qq = forms.CharField(label='QQ', widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    def phone_valid(value):
        mobile_re = re.compile(
            r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
        if not mobile_re.match(value):
            raise ValidationError('手机号码格式错误')
    phone = forms.CharField(label='手机', widget=forms.TextInput(
        attrs={'class': 'form-control'}), validators=[phone_valid, ])

    self_introduction = forms.CharField(
        label="自我介绍", max_length=640, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'cols': 40, 'placeholder': '简单介绍一下自己吧'}))
