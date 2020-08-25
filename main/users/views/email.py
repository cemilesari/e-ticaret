from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, render, redirect, HttpResponse
from django.urls import reverse
from django.conf import settings
from django.views.generic import View


class EmailVerificationSuccess(View):
    template_name = 'accounts/success.html'
    ctx = {}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.ctx)
    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, self.ctx)


class EmailVerificationFailed(View):
    template_name = 'accounts/error.html'
    ctx = {}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.ctx)
    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, self.ctx)
        


class EmailVerificationConfirm(View):
    template_name = 'accounts/confirm.html'
    ctx = {}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.ctx)
    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, self.ctx)
        