from django.contrib import admin
from .models import *
from django import forms

admin.site.site_header = 'XDMSC招新管理'
admin.site.site_title = 'XDMSC招新管理'
admin.site.index_title = 'XDMSC招新管理'

class AnswersInline(admin.TabularInline):
    model = Answers

class ApplicationInline(admin.StackedInline):
    model = Application

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


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'sex', 'email','mentor_list','application', 'c_time', 'has_confirmed')
    list_filter = ('sex', 'status','application',MentorFilter)
    search_fields = ('name',)
    list_per_page = 20
    ordering = ('-c_time',)
    list_editable = ('status',)
    inlines = [ApplicationInline, AnswersInline]

    readonly_fields = ('name', 'sex', 'email', 'birth',
                       'qq', 'phone', 'self_introduction')
    fieldsets = (
        ('基本信息', {
            "fields": (
                'name', 'sex', 'email', 'birth', 'qq', 'phone', 'self_introduction'
            ),
        }),
        ('面试状态', {
            "fields": (
                'status','something'
            ),
        }),
    )

    def group_value(self,obj):
        value = obj.application.group
        return value
    group_value.short_description = "意向部门"

    def mentor_list(self,obj):
        applications=[]
        for app in obj.application.mentor.all():
            applications.append(app.name)
        return ','.join(applications)
    mentor_list.short_description = "意向mentor"

    
    

admin.site.register(User, UserAdmin)

class MessageAdminForm(forms.ModelForm):
    detail = forms.CharField( widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}))
    class Meta:
        model = Questions
        fields = ('__all__')

class MessageAdmin(admin.ModelAdmin):
    form = MessageAdminForm
    list_display = ('title','category','author')
    list_filter = ('category',)
    search_fields = ('title','detail','author')

admin.site.register(Questions, MessageAdmin)


admin.site.register([Category, ConfirmString, Mentor])
