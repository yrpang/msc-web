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
        (1, '一面通过'),
        (2, '一面淘汰'),
        (3, '二面通过'),
        (4, '二面淘汰'),
        (5, '状态待定')
    ]
    status = models.IntegerField(
        "面试状态", choices=STATESCHOICE, blank=False, default=0)
    something = models.CharField("面试备注", max_length=256, blank=True, null=True)

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


class Mentor(models.Model):
    name = models.CharField("姓名", max_length=64)
    def __str__(self):
        return self.name

class Application(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    GROUP = (
        ('活动部', "活动部"),
        ('媒体部', "媒体部"),
        ('技术部', '技术部'),
    )
    group = models.CharField("部门",choices=GROUP, max_length=64, blank=True, null=True)
    mentor = models.ManyToManyField(Mentor,blank=True)
    something = models.CharField("个人简介", max_length=640,default="请介绍一下自己的特长等等")
    stu_num = models.BigIntegerField("学号")
    CHOICE=[
        ('通信工程学院','通信工程学院'),
        ('电子工程学院','电子工程学院'),
        ('计算机科学与技术学院','计算机科学与技术学院'),
        ('机电工程学院','机电工程学院'),
        ('物理与光电工程学院','物理与光电工程学院'),
        ('经济与管理学院','经济与管理学院'),
        ('数学与统计学院','数学与统计学院'),
        ('人文学院','人文学院'),
        ('外国语学院','外国语学院'),
        ('人工智能学院','人工智能学院'),
        ('微电子学院','微电子学院'),
        ('生命科学技术学院','生命科学技术学院'),
        ('空间科学与技术学院','空间科学与技术学院'),
        ('先进材料与纳米科技学院','先进材料与纳米科技学院'),
        ('网络与信息安全学院','网络与信息安全学院'),
        ('国际教育学院','国际教育学院')
    ]
    college = models.CharField("学院",choices=CHOICE,max_length=64,default="通信工程学院")

    def __str__(self):
        if self.group != None:
            return self.group
        else:
            return "未选择"
