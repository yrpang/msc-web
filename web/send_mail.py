from . import models
from django.core.mail import send_mass_mail
from django.conf import settings


receivers = models.User.objects.values_list("email")

receivers = [i[0] for i in receivers]

html_content = '''
                    <table style="width:99.8%;height:99.8%">
    <tbody>
    <tr>
        <td style="background:#fafafa url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAAy0lEQVQY0x2PsQtAYBDFP1keKZfBKIqNycCERUkMKLuSgZnRarIpJX8s3zfcDe9+794du+8bRVHQOI4wDAOmaULTNDDGYFkWMVVVQUTQdZ3iOMZxHCjLElVV0TRNYHVdC7ptW6RpSn3f4wdJkiTs+w6WJAl4DcOAbdugKAq974umaRAEARgXn+cRW3zfFxuiKCJZloXGHMeBbdv4Beq6Duu6Issy7iYB8Jbnucg8zxPLsggnj/zvIxaGIXmeB9d1wSE+nOeZf4HruvABUtou5ypjMF4AAAAASUVORK5CYII=)">
            <div style="border-radius:10px;font-size:15px;color:#555;width:666px;font-family:'Century Gothic','Trebuchet MS','Hiragino Sans GB','微软雅黑','Microsoft Yahei',Tahoma,Helvetica,Arial,SimSun,sans-serif;margin:50px auto;border:1px solid #eee;max-width:100%;background:#fff;box-shadow: 0 2px 5px #00000020;">
                <div style="width:100%;background:#0078D7;color:#fff;border-radius:10px 10px 0 0;background-image:-moz-linear-gradient(left,#0078D7,#16aad8);background-image:-webkit-linear-gradient(left,#0078D7,#16aad8);height:66px"><p style="font-size:18px;word-break:break-all;padding:23px 32px;margin:0;background-color:hsla(0,0%,100%,.4);border-radius:10px 10px 0 0">西电微软俱乐部一面通知</p></div>
                <div style="margin:40px auto;width:90%">
                    <p>各位萌新们：</p>
                    <p>周三晚18:30-22:00将在大活522进行技术部：应用数学组、科研组、GAME组、硬件组、ACM组、web组的面试。<br><br>
                        请大家合理安排时间。无法面试的请戳管理！技术部一面可以去多个部门面试，但是最后只能选择一个组。</p>
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

message = ("西电MSC俱乐部一面通知", "周三晚18:30-22:00将在大活522进行技术部：应用数学组、科研组、GAME组、硬件组、ACM组、web组的免试。请大家合理安排时间。无法免试的请戳管理！技术部一面可以去多个部门免试，但是最后只能选择一个组。", str(settings.EMAIL_HOST_USER), ['yrpang@outlook.com'])


send_mass_mail((message), fail_silently=False)
