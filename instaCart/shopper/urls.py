from django.conf.urls import url

import views

urlpatterns = [
    url(r'^shopper_home/$', views.shopper_home, name='shopper_home'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'), 
    url(r'^register/$', views.register, name='register'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^funnel/$', views.funnel, name='funnel'), 
]