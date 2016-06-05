from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^courses/$', views.courses, name='courses'),
    url(r'^coursesData/$', views.coursesJSON, name='coursesData'),
]
