"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_auth.registration.views import VerifyEmailView, RegisterView
from django.urls import re_path
from main.api.views.user import UpdatePassword,CreateUserView
from allauth.account.views import confirm_email
from allauth.account.views import confirm_email as allauthemailconfirmation
from django.contrib.auth import views as auth_views
from main.users.views import *

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path(settings.ADMIN_URL, admin.site.urls),

    #login && logout added 
    path('api-auth/', include('rest_framework.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    #path('rest-auth/registration/', include('rest_auth.registration.urls')),
    #path('registration/', RegisterView.as_view(), name='account_signup'),
    path('rest-auth/registration/', CreateUserView.as_view(), name="registration"),
    path('rest-auth/change-password', UpdatePassword.as_view(), name="change-password"),
    re_path(r'^account-confirm-email/$', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    re_path(r'^rest-auth/registration/account-confirm-email/(?P<key>\w+)/$', allauthemailconfirmation, name="account_confirm_email"),
    path('account/', include('main.users.urls', namespace="users")),
    path('accounts/', include('django.contrib.auth.urls')),
    path('ckeditor/' , include('ckeditor_uploader.urls')),
    path('api/', include('main.api.urls', namespace="api")),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('main.web.urls', namespace="web")),
    path('reseller/', include('main.reseller.urls', namespace="reseller")),
    path('tickets/', include('main.tickets.urls')),
    path('notify/', include('main.notify.urls')),
    path('reset-password/',auth_views.PasswordResetView.as_view(
      template_name='reset/reset_password.html',
      html_email_template_name='reset/reset_password_email.html',
      token_generator = account_activation_token),
        name='reset_password'
  ),
    path('reset-password-confirmation/<str:uidb64>/<str:token>/',auth_views.PasswordResetConfirmView.as_view(
      template_name='reset/reset_password_update.html', 
      post_reset_login=True,
      post_reset_login_backend='django.contrib.auth.backends.ModelBackend',
      token_generator=account_activation_token,
      success_url =settings.LOGIN_REDIRECT_URL

      ),
        name='password_reset_confirm'
  ),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

