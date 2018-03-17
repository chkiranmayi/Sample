# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf

def login(request):
    token = {}
    token.update(csrf(request))    
    return render_to_response('registration/login.html', token)
    
def process_login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/accounts/loggedin')
    else:
        return HttpResponseRedirect('/accounts/login_error')

def loggedin(request):
    return render_to_response('registration/loggedin.html', 
                              {'username': request.user.username})

def login_error(request):
    return render_to_response('registration/login_error.html')

def logout(request):
    auth.logout(request)
    return render_to_response('registration/logged_out.html')
