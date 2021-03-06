from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('logout', views.logout),
    path('register', views.register),
    path('tests', views.tests),
    path('confirm', views.user_confirm),
    path('application', views.apply),
    path('web4', views.web4),
    path('edit', views.edit),
    path("favicon.ico", RedirectView.as_view(url='static/favicon.ico')),
    path("somehelp", views.help),
    path("dalao", views.Dalao),
]
