# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import Context
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import datetime
import time, json

from shopper.models import Applicant
from shopper.funnel import *

def createSession(request, applicant):
    request.session['first_name'] = applicant.first_name
    request.session['last_name'] = applicant.last_name
    request.session['email'] = applicant.email
    request.session['city'] = applicant.city
    request.session['state'] = applicant.state

def destroySession(request, applicant):
    request.session['first_name'] = None
    request.session['last_name'] = None
    request.session['email'] = None
    request.session['city'] = None
    request.session['state'] = None

# Create your views here.
def shopper_home(request):

    #now = datetime.datetime.now()
    #html = "<html><body>It is now %s.</body></html>" % now
    #return HttpResponse(html)
    if request.session['email'] is None:
        return redirect('login')
    email = request.session['email']
    applicant = Applicant.objects.get(email=email)
    return render(request,'shopper/Aplicant-home.html',applicant.__dict__)


def login(request):

    if request.POST:
        email = request.POST['email']
        try:
            applicant = Applicant.objects.get(email=email)
            createSession(request, applicant)
            return render(request,'shopper/Aplicant-home.html',applicant.__dict__)
        except ObjectDoesNotExist:
            #TODO Message some error
            redirect('login')
        
    
    return render(request,'shopper/login.html')
    #if request.POST:
    #   return render(request,'shopper/login.html')


def logout(request):
    if request.session['email'] is None:
        return redirect('login')
    email = request.session['email']
    applicant = Applicant.objects.get(email=email)
    destroySession(request, applicant)
    return render(request,'shopper/login.html')


def register(request):

    if request.POST:
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        city = request.POST['city']
        state = request.POST['state']
        applicant = Applicant(first_name=first_name, last_name=last_name, email=email, city=city, state=state)
        applicant.save()
        invalidate_cache(timezone.now())
        createSession(request, applicant)
        return redirect('shopper_home')
    
    return render(request,'shopper/register.html')

def edit(request):

    if request.session['email'] is None:
        return redirect('login')
    if request.POST:
        email = request.session['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        city = request.POST['city']
        state = request.POST['state']
        applicant = Applicant.objects.get(email=email)
        applicant.first_name = first_name
        applicant.last_name = last_name
        applicant.city = city
        applicant.state = state
        created_at = timezone.now()
        applicant.save()
        createSession(request, applicant)
        return redirect('shopper_home')
    email = request.session['email']
    applicant = Applicant.objects.get(email=email)
    return render(request,'shopper/edit.html', applicant.__dict__)

def funnel(request):
    #start_date_str="2010-10-01";
    #end_date_str="2014-12-31"
    try:
        request_params = request.GET
        start_date_str = request_params['start_date']
        end_date_str = request_params['end_date']
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str , '%Y-%m-%d').date() 
    except Exception as e:
        return HttpResponseBadRequest(e.message)

    start_time = time.time()
    analytic_metrics=get_analytics(start_date, end_date)
    print("--- %s seconds ---" % (time.time() - start_time))
    return HttpResponse(json.dumps(analytic_metrics), content_type="application/json")


