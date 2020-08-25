from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, render, redirect, HttpResponse
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout, update_session_auth_hash
from django.views.generic import View
from django.contrib.auth.forms import PasswordChangeForm
from main.core.utils import display_form_validations
from main.users.forms import SignUpForm
from main.notify.emails import account_activation

class SignUpView(View):
	user_form = SignUpForm
	initial = {'key': 'value'}
	template_name = 'auth/signup.html'
	def get(self, request, *args, **kwargs):
		user_form = SignUpForm()
		display_form_validations(form = user_form, request= request)
		return render(request, self.template_name, {'user_form' : user_form})
	def post(self, request, *args, **kwargs):
		registered = None 
		user_form = SignUpForm(data = request.POST)
		if user_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			registered = True
			account_activation(user = user)
			print("girdi")
			messages.success(request, 'Registraiton Successful' , extra_tags='success')
			return redirect('users:login')
		else : 
			display_form_validations(form = user_form, request=request)
			user_form = SignUpForm()
		return render(request,self.template_name, {'user_form': user_form, 'registered': registered})


def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
			logout(request)
			messages.success(request, 'Your password was successfully updated!')
			return redirect('users:login')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		form = PasswordChangeForm(request.user)
		return render(request, 'auth/change-password.html', {
		'form': form
	})

