from django.conf.urls import url

import views

urlpatterns = [
    url(r'^shopper_home/$', views.shopper_home, name='shopper_home'),
]