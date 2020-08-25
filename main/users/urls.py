# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.conf.urls import url
from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from main.core.decorators import no_user
from .views import *
app_name = 'users'

urlpatterns = [
    path('login/',                                          view=login_view,                         name="login",),
    path('logout/',                                         view=logout_view,                        name="logout_view",),    
    path('email-verification/<slug:uidb64>/<slug:token>/', 	view=EmailVerification.as_view(),        name='email_verification'),
    path('profile/' ,                                       view=ProfileView.as_view(),              name="profile_view"),
    path('signup/',                                         view=signup,                             name="signup_view"),  
    path('activate/<uidb64>/<token>/' ,                     view=activate,                           name='activate'),  
    path('email-verification/success' ,                     view=EmailVerificationSuccess.as_view(), name='success_page'),
    path('email-verification/failed'  ,                     view=EmailVerificationFailed.as_view(),  name='error_page'),
    path('email-verification/confirm'  ,                    view=EmailVerificationConfirm.as_view(), name='confirm_page'),

]