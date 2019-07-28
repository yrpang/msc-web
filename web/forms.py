from django import forms
from django.forms import formset_factory, ModelForm, modelformset_factory
from .models import Answers, Questions
 
class UserForm(forms.Form):
    email = forms.EmailField(label="邮箱", max_length=128, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    name = forms.CharField(label="姓名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    birth = forms.DateField(label='出生日期', widget=forms.DateInput(format=('%d-%m-%Y'),attrs={'class': 'form-control'}))
    qq = forms.IntegerField(label='QQ', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    phone = forms.IntegerField(label='手机', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    self_introduction = forms.CharField(label="自我介绍", max_length=640, widget=forms.TextInput(attrs={'class': 'form-control'}))

# class AnswersForm(forms.Form):
#     model = Answers
#     fields = ['answer']
# AnswersFormSet=formset_factory(AnswersForm, )

class AnswersForm(forms.ModelForm):
    
    class Meta:
        model = Answers
        fields = ("answer","question")
AnswersFormSet = modelformset_factory(Answers, form=AnswersForm)

class QuestionsForm(forms.ModelForm):
    # answers = Answers.objects,filter()
    class Meta:
        model = Questions
        fields = ("title", "detail")
QuestionsFormSet = modelformset_factory(Questions, form=QuestionsForm)


class AnswerForm(forms.Form):
    answer = forms.CharField(label="你的答案")
AnswerFormSet = formset_factory(AnswerForm)
