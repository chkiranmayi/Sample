import views
from django.conf.urls import url

urlpatterns = [

    url(r'^accounts/login/$', views.login),
    url(r'^accounts/process_login/$', views.process_login),
    url(r'^accounts/loggedin/$', views.loggedin),
    url(r'^accounts/login_error/$', views.login_error),
    url(r'^accounts/logout/$', views.logout),
]
