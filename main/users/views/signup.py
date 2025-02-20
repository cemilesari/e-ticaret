from django.http import HttpResponse  
from django.shortcuts import render  
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string
from main.users.forms import SignUpForm 
from .tokens import account_activation_token  
from main.users.models import User  
from django.core.mail import EmailMessage
from django.shortcuts import HttpResponseRedirect, render, redirect, HttpResponse
from django.urls import reverse

def signup(request):  
    if request.method == 'GET':  
        return render(request, 'auth/signup.html')  
    if request.method == 'POST':  
        form = SignUpForm(request.POST)  
        # print(form.errors.as_data())  
        if form.is_valid():  
            user = form.save(commit=False)  
            user.is_active = False  
            user.save()  
            current_site = get_current_site(request)  
            mail_subject = 'Activate your account.'  
            message = render_to_string('accounts/acc_active_email.html', {  
                'user': user,  
                'domain': 'test.yemekkalmasin.com',  
                'uid': urlsafe_base64_encode(force_bytes(user.id)),  
                'token': account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                mail_subject, message, to=[to_email]  
            )  
            email.send()  
            return redirect(reverse("users:confirm_page"))  
        else:  
            form = SignUpForm()  
            return render(request, 'auth/signup.html', {'form': form})
def activate(request, uidb64, token):  
        try:  
            uid = force_text(urlsafe_base64_decode(uidb64))  
            user = User.objects.get(id=uid)  
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
            user = None  
        if user is not None and account_activation_token.check_token(user, token):  
            user.is_active = True 
            user.is_email  = True
            user.save()  
            print(user)
            print(token)
            return redirect(reverse("users:success_page"))  
        else:  
            return redirect(reverse("users:error_page"))