from django.shortcuts import render,redirect
from . import models
from .forms import UserForm, RegisterForm, AnswersFormSet, QuestionsFormSet, AnswerFormSet, AnswerForm
import hashlib
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.forms import formset_factory


 
def hash_code(s, salt='mysite'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()
 
def index(request):
    pass
    return render(request,'index.html')
 

def login(request):
    if request.session.get('is_login',None):
        return redirect('/index')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(email=email)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login/login.html', locals())
 
    login_form = UserForm()
    return render(request, 'login/login.html', locals())
 
def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            name = register_form.cleaned_data['name']
            sex = register_form.cleaned_data['sex']
            email = register_form.cleaned_data['email']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            birth = register_form.cleaned_data['birth']
            qq = register_form.cleaned_data['qq']
            phone = register_form.cleaned_data['phone']
            self_introduction = register_form.cleaned_data['self_introduction']

            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())
 
                # 当一切都OK的情况下，创建新用户

                new_user = models.User.objects.create(name=name, password=hash_code(password1), email=email, sex=sex, phone=phone, qq=qq, self_introduction=self_introduction, birth=birth)

                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())
 
def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/")
    request.session.flush()
    return redirect("/")


def tests(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")

    count = models.Questions.objects.count()
    

    AnswerFormSet = formset_factory(AnswerForm, extra=2, max_num=count)

    if request.method == 'POST':
        ans = AnswerFormSet(request.POST)
        
        ans=ans.cleaned_data
        user = models.User.objects.get(id=request.session.get('user_id'))
        question = models.Questions.objects.all().order_by('id')

        for i in range(count):
            if ans[i]:
                try:
                    a=models.Answers.objects.get(user__id=request.session.get('user_id'), question=question[i])
                    a.answer = ans[i]['answer']
                    a.save()
                except models.Answers.DoesNotExist:
                    models.Answers.objects.create(user = user, question=question[i],answer=ans[i]['answer'])
            else:
                models.Answers.objects.create(user = user, question=question[i], answer=" ")
        formset = AnswerFormSet(request.POST)
        return render(request, 'tests.html', locals())
        

    ans = models.Answers.objects.filter(user__id = request.session.get('user_id')).order_by('question__id')

    ini = [{'answer': i.answer} for i in ans]

    

    formset = AnswerFormSet(initial=ini)
    question = models.Questions.objects.all().order_by('id')

    return render(request, 'tests.html', locals())

    


#     # formset = QuestionsFormSet(queryset=models.Questions.objects.filter(answers__user__id=request.session.get('user_id')))
#     # formset = AnswersFormSet(queryset=models.Answers.objects.filter(user__id=request.session.get('user_id')))

#     web = models.Questions.objects.all()

#     return render(request, 'tests.html', locals())


# def answer(request, user_id):
#     if request.method == "GET":
#         return HttpResponseForbidden()

#     try:
#         user = models.User.objects.get(id=user_id)
#     except models.User.DoesNotExist:
#         return HttpResponseForbidden()


# 尝试手动建立动态表单 没成功
    # ans = request.POST.dict()
    # ans.pop('csrfmiddlewaretoken')

    # for i in ans:
    #     try:
    #         question= models.Questions.objects.get(id = i)
    #     except models.Questions.DoesNotExist:
    #         return HttpResponseForbidden()
        
    #     try:
    #         tem = models.Answers.objects.get(user = user, question=question)
    #         tem.answer = ans[i]
    #         tem.save()
    #     except models.Answers.DoesNotExist:
    #         models.Answers.objects.create(user=user, question=question, answer=ans[i])
    #     print(locals())


# 尝试使用FormSet建立动态表单 没成功
    # AnswerSet = AnswersFormSet(request.POST)
    # for i in AnswerSet:
    #     i.instance.user = user # 要实例化才行
    #     i.save()
    #     print(i)



    # return redirect("/tests/")
