import csv
from django.shortcuts import render, redirect
from . import models
from .forms import UserForm, RegisterForm, ApplicationForm, EditForm
import hashlib
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.forms import formset_factory, Form, fields, widgets
import datetime
from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMultiAlternatives, send_mail
import requests
import json
from django.contrib.admin.models import LogEntry


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
        return redirect('/')

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

    subject = 'XDMSC注册确认'

    text_content = '欢迎加入XDMSC的大家庭，请复制链接https://{}/confirm?code={} 到浏览器进行确认，有效期3天'.format(
        'www.xdmsc.club', code)

    html_content = '''
                    <p>欢迎加入XDMSC大家庭</p>
                    <p>请点击链接<a href="https://{}/confirm?code={}" target=blank>https://{}/confirm?code={}</a>完成注册确认！</p>
                    <p>此链接有效期为3天！</p>
                    '''.format('www.xdmsc.club', code, 'www.xdmsc.club', code)

    msg = EmailMultiAlternatives(
        subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def register(request):
    
    return render(request, 'login/hasend.html')
    if request.session.get('is_login', None):
        return redirect("/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "填写错误，请检查"
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
                return redirect('/login')  # 自动跳转到登录页面
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
        return redirect("/login")
    field_dict = {}
    question = models.Questions.objects.all().order_by('id')
    for q in question:
        field_dict['%s_%s' % (q.category.name, q.id)] = fields.CharField(
            required=False,
            label=q.title,
            help_text=q.detail,
            widget=widgets.Textarea(
                attrs={'class': 'form-control', 'rows': 6, 'cols': 40})
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
        return render(request, 'tests.html', {'formset': formset, 'dis': ['id_媒体部_12', 'id_媒体部_14', 'id_媒体部_15', 'id_硬件_4']})

    elif request.method == 'POST':
        ans = MyAnswerForm(request.POST)
        user = models.User.objects.get(id=request.session.get('user_id'))

        if ans.is_valid():
            ans = ans.cleaned_data

            for key, v in ans.items():
                k, qid = key.rsplit('_', 1)
                if v == "":
                    continue
                try:
                    a = models.Answers.objects.get(question__id=qid, user=user)
                    a.answer = v
                    a.save()
                except models.Answers.DoesNotExist:
                    q = models.Questions.objects.get(id=qid)
                    models.Answers.objects.create(
                        user=user, question=q, answer=v)
        formset = MyAnswerForm(request.POST)
        return render(request, 'tests.html', {'formset': formset, 'dis': ['id_媒体部_12', 'id_媒体部_14', 'id_媒体部_15', 'id_硬件_4'], 'message': '保存成功！'})


@csrf_exempt
def web4(request):
    if request.method == 'GET':
        return render(request, 'web4.html')
    elif request.method == 'POST':
        ans = request.POST.get('year', None)
        if ans == '2019':
            print(ans)
            return render(request, 'web4.html', {'flag': 'flag{just_P0st}'})
        else:
            return render(request, 'web4.html')


def apply(request):
    if not request.session.get('is_login', None):
        return redirect("/login")
    if request.method == 'GET':
        try:
            data = models.Application.objects.get(
                user__id=request.session.get('user_id'))
            app = ApplicationForm(instance=data)
        except:
            app = ApplicationForm()
        return render(request, 'applications.html', locals())
    elif request.method == 'POST':
        try:
            data = models.Application.objects.get(
                user__id=request.session.get('user_id'))
            app = ApplicationForm(instance=data, data=request.POST)
        except:
            app = ApplicationForm(request.POST)
        if app.is_valid():
            if app.cleaned_data['mentor'].count() > 3:
                message = "不要太贪心呀，最多选三个mentor哦！"
                return render(request, 'applications.html', locals())
            a = app.save(commit=False)
            a.user = models.User.objects.get(id=request.session.get('user_id'))
            a.save()
            app.save_m2m()
            message = "您的信息已保存"
        else:
            message = "学号填写错误"
            error = app.errors
        return render(request, 'applications.html', locals())


def edit(request):
    if not request.session.get('is_login', None):
        return redirect("/")
    if request.method == "GET":
        data = models.User.objects.get(id=request.session.get('user_id'))

        initial = {
            "email": data.email,
            "name": data.name,
            "sex": data.sex,
            "birth": data.birth,
            "qq": data.qq,
            "phone": data.phone,
            "self_introduction": data.self_introduction
        }
        edit_form = EditForm(initial=initial)
        return render(request, 'login/edit.html', locals())
    elif request.method == "POST":
        edit_form = EditForm(request.POST)
        try:
            user = models.User.objects.filter(
                id=request.session.get('user_id'))
        except:
            message = "用户不存在"
            return render(request, 'login/edit.html', locals())
        if edit_form.is_valid():  # 获取数据
            sex = edit_form.cleaned_data['sex']
            password1 = edit_form.cleaned_data['password1']
            password2 = edit_form.cleaned_data['password2']
            birth = edit_form.cleaned_data['birth']
            qq = edit_form.cleaned_data['qq']
            phone = edit_form.cleaned_data['phone']
            self_introduction = edit_form.cleaned_data['self_introduction']

            user.update(sex=sex, phone=phone, qq=qq,
                        self_introduction=self_introduction, birth=birth)

            if password1 != '':
                if password1 != password2:  # 判断两次密码是否相同
                    message = "两次输入的密码不同！"
                    return render(request, 'login/edit.html', locals())
                else:
                    a = user[0]
                    a.password = hash_code(password1)
                    a.save()
                    request.session.flush()
                    return redirect('/login')

            return redirect('/')

        else:
            error = edit_form.errors
            return render(request, 'login/edit.html', locals())


def help(request):
    return render(request, "help.html")


def send_magic_code(email, code, mentorname: str):

    subject = 'XDMSC神秘代码'

    text_content = '恭喜获得{}提供的一面免试资格，请复制链接https://{}/dalao?magiccode={} 激活你的神秘代码，有效期3天'.format(
        mentorname, 'www.xdmsc.club', code)

    html_content = '''
                    <p>恭喜获得神秘代码</p>
                    <p>恭喜你获得mentor{}提供的一面免试资格,请点击链接<a href="https://{}/dalao?magiccode={}" target=blank>https://{}/dalao?magiccode={}</a>完成确认！</p>
                    <p>此链接有效期为3天！</p>
                    '''.format(mentorname, 'www.xdmsc.club', code, 'www.xdmsc.club', code)
    msg = EmailMultiAlternatives(
        subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def make_dalao_string(user, mentorname: str):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    try:
        t = models.DalaoString.objects.get(user=user)
        t.delete()
        models.DalaoString.objects.create(code=code, user=user)
    except models.DalaoString.DoesNotExist:
        t = models.DalaoString.objects.create(code=code, user=user)
    send_magic_code(user.email, code, mentorname)


def send_qq_message(message: str):
    url = 'http://127.0.0.1:5700/send_group_msg'
    headers = {'Content-Type': 'application/json'}
    data = {"group_id": 839637019, "message": message}
    requests.post(url=url, data=json.dumps(data), headers=headers)


def Dalao(request):
    code = request.GET.get('magiccode', None)
    message = ''
    try:
        magic_code = models.DalaoString.objects.get(code=code)
    except:
        message = '你输入的神秘代码无效哦，请联系mentor检查'
        return render(request, 'dalao.html', locals())

    c_time = magic_code.c_time
    now = timezone.now()
    if now > c_time + datetime.timedelta(3):
        magic_code.delete()
        message = '您的神秘代码已过期，请联系mentor重新索要'
        return render(request, 'dalao.html', locals())
    elif magic_code.user.if_dalao == True:
        message = '您已经验证过了，无需重复操作！'
        return render(request, 'dalao.html', locals())
    else:
        magic_code.user.if_dalao = True
        magic_code.user.status = 1
        name = magic_code.user.name
        magic_code.user.save()
        magic_code.delete()
        message = '神秘代码验证通过，恭喜你获得免一面资格，请准时来参加二面哦！'
        send_qq_message("恭喜%s获得一面免试资格" % name)
        return render(request, 'dalao.html', locals())


def send_time_mail(email: list):

    subject = '西电MSC技术部web组二面通知'

    html_content = '''
                <table style="width:99.8%;height:99.8%">
    <tbody>
    <tr>
        <td style="background:#fafafa url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAAy0lEQVQY0x2PsQtAYBDFP1keKZfBKIqNycCERUkMKLuSgZnRarIpJX8s3zfcDe9+794du+8bRVHQOI4wDAOmaULTNDDGYFkWMVVVQUTQdZ3iOMZxHCjLElVV0TRNYHVdC7ptW6RpSn3f4wdJkiTs+w6WJAl4DcOAbdugKAq974umaRAEARgXn+cRW3zfFxuiKCJZloXGHMeBbdv4Beq6Duu6Issy7iYB8Jbnucg8zxPLsggnj/zvIxaGIXmeB9d1wSE+nOeZf4HruvABUtou5ypjMF4AAAAASUVORK5CYII=)">
            <div style="border-radius:10px;font-size:15px;color:#555;width:666px;font-family:'Century Gothic','Trebuchet MS','Hiragino Sans GB','微软雅黑','Microsoft Yahei',Tahoma,Helvetica,Arial,SimSun,sans-serif;margin:50px auto;border:1px solid #eee;max-width:100%;background:#fff;box-shadow: 0 2px 5px #00000020;">
                <div style="width:100%;background:#0078D7;color:#fff;border-radius:10px 10px 0 0;background-image:-moz-linear-gradient(left,#0078D7,#16aad8);background-image:-webkit-linear-gradient(left,#0078D7,#16aad8);height:66px"><p style="font-size:18px;word-break:break-all;padding:23px 32px;margin:0;background-color:hsla(0,0%,100%,.4);border-radius:10px 10px 0 0">西电MSC技术部web组二面通知</p></div>
                <div style="margin:40px auto;width:90%">
                    <p>同学你好:</p>
                    <p>恭喜你成功通过技术部web组第一次面试，我们计划于本周二9月24日下午18:00至晚上21：00进行技术部web的第二次面试，具体地点请关注招新群通知，若时间有冲突，请尽快于招新群【272522614】内联系"895808228 庞义人"</p>
                    <p style="border-bottom-right-radius: 2px;border-left: 4px solid #f66;border-top-right-radius: 2px;margin: 2em 0;padding: 12px 24px 12px 30px;position: relative;background-color: #f8f8f8;">
                            请注意：此邮件为系统自动发送，请勿直接回复。<br>
                            若此邮件不是您请求的，请忽略并删除！</p>
                </div>
            </div>
        </td>
    </tr>
    </tbody>
</table>
                '''

    try:
        send_mail(
            '西电MSC技术部web组二面通知', '恭喜你成功通过技术部web组第一次面试，我们计划于本周二9月24日下午18:00至晚上21：00进行技术部web组的第二次面试，具体地点请关注招新群通知，若时间有冲突，请尽快于招新群【272522614】内联系"895808228 庞义人"。', settings.EMAIL_HOST_USER, email, html_message=html_content)
    except Exception as e:
        print(e)


def export_excel():
    with open('result1.csv', 'w') as f:
        writer = csv.writer(f)
        data = models.User.objects.filter(has_confirmed=True).values_list(
            'email', 'name', 'sex','application__mentor__name', 'application__group','status','if_dalao', 'something')
        # data = LogEntry.objects.all().order_by('action_time').values_list('user__last_name','user__first_name','object_repr','change_message','action_time')
        
        for i in data:
            writer.writerow(i)
