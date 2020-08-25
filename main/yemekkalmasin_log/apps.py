from __future__ import unicode_literals, absolute_import
from django.apps import AppConfig 
from django.utils.translation import ugettext_lazy as _ 

class YemekkalmasinLogConfig(AppConfig):
    name = "main.yemekkalmasin_log"
    verbose_name = _("Yemek Kalmasin Logs")
