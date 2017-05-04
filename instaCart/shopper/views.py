# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import datetime
from django.http import HttpResponse


# Create your views here.

def shopper_home(request):

    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def login(request):
    html = "<html><body>It is now login page.</body></html>" 
    return HttpResponse(html)

def logout(request):
    html = "<html><body>It is now logout page.</body></html>" 
    return HttpResponse(html)

def register(request):
    html = "<html><body>It is now register page.</body></html>" 
    return HttpResponse(html)

def edit(request):
    html = "<html><body>It is now edit page.</body></html>" 
    return HttpResponse(html)