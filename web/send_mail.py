from . import models
from django.core.mail import send_mass_mail
from django.conf import settings


receivers = models.User.objects.values_list("email")

receivers = [i[0] for i in receivers]

html_content = '''
                    <p>西电MSC俱乐部一面通知</p>
                    <p>各位萌新们：</p>
                    <p>    周三晚18:30-22:00将在大活522进行技术部：应用数学组、科研组、GAME组、硬件组、ACM组、web组的免试。</p>
                    <p>    请大家合理安排时间。无法免试的请戳管理！技术部一面可以去多个部门免试，但是最后只能选择一个组。</p>
                '''

message = ("西电MSC俱乐部一面通知", "周三晚18:30-22:00将在大活522进行技术部：应用数学组、科研组、GAME组、硬件组、ACM组、web组的免试。请大家合理安排时间。无法免试的请戳管理！技术部一面可以去多个部门免试，但是最后只能选择一个组。", str(settings.EMAIL_HOST_USER), ['yrpang@outlook.com'])


send_mass_mail((message), fail_silently=False)
