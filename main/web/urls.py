# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.conf.urls import url
from django.urls import path, re_path

from .views import *

app_name = 'web'

urlpatterns = [
	path('manage/'        , global_manage  , name='global_manage'),
	path(''               , view= BestSellers.as_view()      , name='home_view'),
]