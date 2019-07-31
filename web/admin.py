from django.contrib import admin
from .models import *
from django import forms

admin.site.site_header = 'XDMSC招新管理'
admin.site.site_title = 'XDMSC招新管理'
admin.site.index_title = 'XDMSC招新管理'

class AnswersInline(admin.TabularInline):
    model = Answers


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'sex', 'email', 'c_time', 'has_confirmed')
    list_filter = ('sex', 'status')
    search_fields = ('name',)
    list_per_page = 20
    ordering = ('-c_time',)
    list_editable = ('status',)
    inlines = [AnswersInline]

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


admin.site.register(User, UserAdmin)

class MessageAdminForm(forms.ModelForm):
    detail = forms.CharField( widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}))
    class Meta:
        model = Questions
        fields = ('__all__')

class MessageAdmin(admin.ModelAdmin):
    form = MessageAdminForm
admin.site.register(Questions, MessageAdmin)


admin.site.register([Category, ConfirmString])
