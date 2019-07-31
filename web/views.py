from django.shortcuts import render, redirect
from . import models
from .forms import UserForm, RegisterForm
import hashlib
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.forms import formset_factory, Form, fields, widgets
import datetime
from django.conf import settings
from django.utils import timezone


def hash_code(s, salt='mysite'):  # 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def index(request):
    pass
    return render(request, 'index.html')


def login(request):
    if request.session.get('is_login', None):
        return redirect('/index')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(email=email)
                if not user.has_confirmed:
                    message = '您还未经过邮件确认，请检查您的注册邮箱！'
                    return render(request, 'login/login.html', locals())
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


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user,)
    return code


def send_email(email, code):

    from django.core.mail import EmailMultiAlternatives

    subject = 'XDMSC注册确认'

    text_content = '欢迎加入XDMSC的大家庭，请复制链接https://{}/confirm/?code={} 到浏览器进行确认，有效期3天'.format(
        'demo.pangyiren.com', code)

    html_content = '''
                    <p>欢迎加入XDMSC大家庭</p>
                    <p>请点击链接<a href="https://{}/confirm/?code={}" target=blank>https://{}/confirm/?code={}</a>完成注册确认！</p>
                    <p>此链接有效期为3天！</p>
                    '''.format('www.xdmsc.club', code, 'www.xdmsc.club', code)

    msg = EmailMultiAlternatives(
        subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def register(request):
    if request.session.get('is_login', None):
        return redirect("/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "未知错误，请联系管理"
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
                print(same_email_user)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.User.objects.create(name=name, password=hash_code(
                    password1), email=email, sex=sex, phone=phone, qq=qq, self_introduction=self_introduction, birth=birth)

                code = make_confirm_string(new_user)
                send_email(email, code)
                return redirect('/login/')  # 自动跳转到登录页面
        else:
            error = register_form.errors
            return render(request, 'login/register.html', locals())
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    now = timezone.now()
    if now > c_time + datetime.timedelta(3):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'login/confirm.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/")
    request.session.flush()
    return redirect("/")


def tests(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    field_dict = {}
    question = models.Questions.objects.all().order_by('id')
    for q in question:
        field_dict['%s_%s' % (q.category.name, q.id)] = fields.CharField(
            required=False,
            label=q.title,
            help_text=q.detail,
            widget=widgets.TextInput(attrs={'class': 'form-control'})
        )

    MyAnswerForm = type('MyAnswerForm', (Form,), field_dict)

    if request.method == 'GET':
        ini = {}
        for q in question:
            try:
                a = models.Answers.objects.get(
                    user__id=request.session.get('user_id'), question=q)
                ini['%s_%s' % (q.category.name, q.id)] = a.answer
            except models.Answers.DoesNotExist:
                ini['%s_%s' % (q.category.name, q.id)] = ""

        formset = MyAnswerForm(initial=ini)
        return render(request, 'tests.html', {'formset': formset,'num':range(1,13)})

    else:
        ans = MyAnswerForm(request.POST)
        user = models.User.objects.get(id=request.session.get('user_id'))

        if ans.is_valid():
            ans = ans.cleaned_data

            for key, v in ans.items():
                k, qid = key.rsplit('_', 1)
                try:
                    a = models.Answers.objects.get(question__id=qid, user=user)
                    a.answer = v
                    a.save()
                except models.Answers.DoesNotExist:
                    q = models.Questions.objects.get(id=qid)
                    models.Answers.objects.create(
                        user=user, question=q, answer=v)
        formset = MyAnswerForm(request.POST)
        return render(request, 'tests.html', {'formset': formset})
