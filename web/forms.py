from django import forms
from django.forms import formset_factory, ModelForm, modelformset_factory, widgets
from .models import Answers, Questions, Application
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
        format=('%Y-%m-%d'), attrs={'class': 'form-control', 'placeholder': '1999-01-01'}))
    qq = forms.CharField(label='QQ', widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    def phone_valid(value):
        mobile_re = re.compile(
            r'1[0-9]{10}$')
        if not mobile_re.match(value):
            raise ValidationError('手机号码格式错误')
    phone = forms.CharField(label='手机', widget=forms.TextInput(
        attrs={'class': 'form-control'}), validators=[phone_valid, ])

    self_introduction = forms.CharField(error_messages={'invalid': '请填写自我介绍', 'null': '请填写自我介绍', 'blank': '请填写自我介绍'},
                                        label="自我介绍", max_length=640, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'cols': 40, 'placeholder': '简单介绍一下自己吧'}))


class ApplicationForm(forms.ModelForm):
    def clean_stu_num(self):
        value = self.cleaned_data.get('stu_num')
        mobile_re = re.compile(
            r'1[0-9]{10}$')
        if not mobile_re.match(str(value)):
            raise ValidationError('学号错误')
        else:
            return value

    class Meta:
        model = Application
        fields = ("stu_num", "college", "group", "mentor", "something")
        widgets = {
            'stu_num': forms.TextInput(attrs={'class': 'form-control'}),
            'college': forms.Select(attrs={'class': 'selectpicker form-control'}),
            'group': forms.Select(attrs={'class': 'selectpicker form-control', 'id': 'group_select'}),
            'mentor': forms.SelectMultiple(attrs={'class': 'selectpicker form-control', 'multiple': '', 'title': '请选择mentor', 'id': 'mentor_select', 'data-live-search': 'true'}),
            'something': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'cols': 40, 'placeholder': '请介绍一下自己的特长等等'})
        }


class EditForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    name = forms.CharField(label="姓名", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control', 'readonly': 'readonly'}))
    sex = forms.ChoiceField(label='性别', choices=gender,
                            widget=forms.Select(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(
        attrs={'class': 'form-control', 'readonly': 'readonly'}))
    password1 = forms.CharField(label="密码", max_length=256, required=False, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '留空不修改'}))
    password2 = forms.CharField(label="确认密码", max_length=256, required=False, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    birth = forms.DateField(error_messages={'invalid': '出生日期格式错误 正确样例1999-01-01'}, label='出生日期', widget=forms.DateInput(
        format=('%Y-%m-%d'), attrs={'class': 'form-control', 'placeholder': '1999-01-01'}))
    qq = forms.CharField(label='QQ', widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    def phone_valid(value):
        mobile_re = re.compile(
            r'1[0-9]{10}$')
        if not mobile_re.match(value):
            raise ValidationError('手机号码格式错误')
    phone = forms.CharField(label='手机', widget=forms.TextInput(
        attrs={'class': 'form-control'}), validators=[phone_valid, ])

    self_introduction = forms.CharField(
        label="自我介绍", max_length=640, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'cols': 40, 'placeholder': '简单介绍一下自己吧'}))
