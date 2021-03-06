from django.contrib import admin
from .models import *
from django import forms
from mdeditor.widgets import MDEditorWidget
from django.db import models
from .views import make_dalao_string

admin.site.site_header = 'XDMSC招新管理'
admin.site.site_title = 'XDMSC招新管理'
admin.site.index_title = 'XDMSC招新管理'


class AnswersInline(admin.StackedInline):
    model = Answers
    fields = ['answer', ]

    def get_queryset(self, request):
        qs = super(AnswersInline, self).get_queryset(request)
        return qs.order_by('question__category')

class AppForm(forms.ModelForm):
    # status = forms.Select(widget=forms.RadioSelect())
    class Meta:
        model = Application
        fields = ['mentor']
        # widgets = {
        #     'status': forms.Select()
        # }
 



class ApplicationInline(admin.TabularInline):
    model = Application
    readonly_fields=['something','stu_num','college']
    # form = AppForm


class MentorFilter(admin.SimpleListFilter):
    title = "Mentor"
    parameter_name = "mentor"

    def lookups(self, request, model_admin):
        mentor = Mentor.objects.all()
        mentor = set([m for m in mentor])
        return [(m.name, m.name) for m in mentor]

    def queryset(self, request, queryset):
        if not self.value():
            return queryset.all()
        else:
            return queryset.filter(application__mentor__name__contains=self.value())


class GroupFilter(admin.SimpleListFilter):
    title = "部门"
    parameter_name = "group"

    def lookups(self, request, model_admin):
        group = Application.objects.values("group").all()
        group = set([g.get('group') for g in group])
        return [(g, g) for g in group]

    def queryset(self, request, queryset):
        if not self.value():
            return queryset.all()
        else:
            return queryset.filter(application__group__contains=self.value())

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['status']
        widgets = {
            'status': forms.RadioSelect()
        }
 

class UserAdmin(admin.ModelAdmin):
    form = UserForm
    list_display = ('name', 'status', 'sex', 'email',
                    'mentor_list', 'application', 'c_time', 'has_confirmed', 'if_dalao')
    list_filter = ('sex', 'status', GroupFilter, MentorFilter)
    search_fields = ('name','qq','phone')
    list_per_page = 20
    ordering = ('-c_time',)
    list_editable = ('status',)
    inlines = [ApplicationInline, AnswersInline]
    actions = ['set_as_dalao']

    # readonly_fields = ('name', 'sex', 'email', 'birth',
    #                    'qq', 'phone', 'self_introduction')
    fieldsets = (
        ('基本信息', {
            "fields": (
                'name', 'sex', 'email', 'birth', 'qq', 'phone', 'self_introduction'
            ),
        }),
        ('面试状态', {
            "fields": (
                'status', 'something','has_confirmed'
            ),
        }),
    )

    def group_value(self, obj):
        value = obj.application.group
        return value
    group_value.short_description = "意向部门"

    def mentor_list(self, obj):
        applications = []
        for app in obj.application.mentor.all():
            applications.append(app.name)
        return ','.join(applications)
    mentor_list.short_description = "意向mentor"

    def set_as_dalao(self, request, queryset):
        name = request.user.last_name + request.user.first_name
        for i in queryset:
            make_dalao_string(i, name)
    # 指定后台界面动作的关键词
    set_as_dalao.short_description = "生成免试码"


admin.site.register(User, UserAdmin)


class MessageAdminForm(forms.ModelForm):
    detail = forms.CharField(widget=MDEditorWidget)

    class Meta:
        model = Questions
        fields = ('__all__')


class MessageAdmin(admin.ModelAdmin):
    form = MessageAdminForm
    list_display = ('title', 'category', 'author')
    list_filter = ('category',)
    search_fields = ('title', 'detail', 'author')


admin.site.register(Questions, MessageAdmin)


admin.site.register([Category, ConfirmString, Mentor, DalaoString])
