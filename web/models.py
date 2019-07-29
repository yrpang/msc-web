from django.db import models
import django.utils.timezone as timezone


class User(models.Model):
    name = models.CharField("姓名", max_length=64, blank=False)
    GENDER = [
        ('male', "男"),
        ('female', "女"),
    ]
    sex = models.CharField("性别", choices=GENDER, blank=False, max_length=32)
    email = models.EmailField("邮箱", unique=True, blank=False)
    password = models.CharField("密码", max_length=256, blank=False)
    birth = models.DateField("出生日期", blank=False)
    qq = models.CharField("QQ", max_length=64, blank=False)
    phone = models.CharField("手机号", max_length=64, blank=False)
    self_introduction = models.CharField("自我介绍", max_length=2000, blank=False)
    c_time = models.DateTimeField("注册时间", auto_now_add=True)
    has_confirmed = models.BooleanField("是否已经邮件确认",default=False)

    STATESCHOICE = [
        (0, '等待面试'),
        (1, '通过'),
        (2, '淘汰'),
        (3, '待定'),
    ]
    status = models.IntegerField(
        "面试状态", choices=STATESCHOICE, blank=False, default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-c_time']
        verbose_name = '面试名单'
        verbose_name_plural = '面试名单'


class Category(models.Model):
    name = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = "分类"

    def __str__(self):
        return self.name


class Questions(models.Model):
    title = models.CharField("题目", max_length=256, blank=False)
    detail = models.CharField("题目描述", blank=False, max_length=1200)
    author = models.CharField("出题人", blank=True, null=True, max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '福利题'
        verbose_name_plural = '福利题'


class Answers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(
        Questions, on_delete=models.CASCADE, related_name="ans")
    answer = models.CharField(blank=False, max_length=1200)
    c_time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.question.title

    class Meta:
        ordering = ['-c_time']
        verbose_name = '作答'
        verbose_name_plural = '作答'


class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name + ":   " + self.code

    class Meta:

        ordering = ["-c_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"
