from django import template
from django.utils.safestring import mark_safe
   
register = template.Library()  # 固定写法

@register.filter
def f1(value):
    
    value = value.split('_')
    return value[1]

@register.filter
def error_msg(error_list):
    r=[]
    if error_list:
        for i in error_list:
            r.append(error_list[i])
        return r
        