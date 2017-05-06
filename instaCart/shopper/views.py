# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import Context
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib import messages
from django.db import IntegrityError


import datetime
import time, json

from shopper.models import Applicant
from shopper.funnel import *

## Util function to create and destroy functions
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

def index(request):
    # This is the landing page, it just redirects to the home page
   return render(request,'shopper/landing.html')
   
def shopper_home(request):
    # A shopper lands here either after logging in or after registration
    if request.session['email'] is None:
        return redirect('login')
    email = request.session['email']
    applicant = Applicant.objects.get(email=email)
    return render(request,'shopper/applicant_home.html',applicant.__dict__)


def login(request):
    # Triggered by login request, if the email id doesn't exists, then return
    # error, otherwise success
    if request.POST:
        email = request.POST['email']
        try:
            applicant = Applicant.objects.get(email=email)
            createSession(request, applicant)
            return redirect('shopper_home')
        except ObjectDoesNotExist:
            error_message ="User does not exist"
            messages.add_message(request, messages.ERROR, error_message)
            errorObj = {}
            errorObj['invalidEmail'] = email
            return render(request,'shopper/landing.html', errorObj)
        
    #For get requests just redirect to landing page
    return render(request,'shopper/landing.html')



def logout(request):
    # Destroy the session if already logged in
    if request.session['email'] is None:
        return redirect('login')
    email = request.session['email']
    applicant = Applicant.objects.get(email=email)
    destroySession(request, applicant)
    return render(request,'shopper/landing.html')


def register(request):
    # If email is unique then register, otherwise error
    if request.POST:
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        city = request.POST['city']
        state = request.POST['state']
        applicant = Applicant(first_name=first_name, last_name=last_name, email=email, city=city, state=state)
        try:
            applicant.save()
        except IntegrityError:
            error_message ="Email already exists"
            print error_message
            messages.add_message(request, messages.ERROR, error_message)
            return render(request,'shopper/landing.html',  applicant.__dict__)
        invalidate_cache(timezone.now())
        createSession(request, applicant)
        return redirect('shopper_home')
    
    return render(request,'shopper/landing.html')


def edit(request):
    # Check if logged in, if logged in then 
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

    # If a separate edit page was used, then the get request would have been
    # used to render edit form. But now I am using modal, hence the code below
    # is no-op.
    email = request.session['email']
    applicant = Applicant.objects.get(email=email)
    return render(request,'shopper/applicant_home.html', applicant.__dict__)

def funnel(request):
    # Funnel API to get the metrics. It will try to first convert the dates
    # If successful, it asks Funnel module for the analytics else errors
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


