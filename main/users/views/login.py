
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, render, redirect, HttpResponse
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required

from main.users.backends.auth_backends import lang_authenticate
from main.users.forms import SignInForm
from main.core.utils import display_form_validations

def login_view(request):
    username = email_yok = None
    form = SignInForm(request.POST)
    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        if form.is_valid():
            user = lang_authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    #if not user.is_email:
                        #messages.warning(request, _("Your Email Address is not verified yet! please verify your email address."))
                        #email_yok = True
                        #username = str(user.username)
                    #else:
                    login(request,user)
                    request.session['yemekkalmasın_sess'] = ''
                    return redirect('/')
                else:
                    messages.warning(request, _('User banned, please contact support'))
            else:
                messages.error(request, _('Login Error, Invalid username or password, please try again'))
        else:
            display_form_validations(form=form, request=request)
            
    return render(request, "auth/login.html", dict(email_yok=email_yok, username=username,))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')