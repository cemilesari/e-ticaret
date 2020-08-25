from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
import logging
from crequest.middleware import CrequestMiddleware

from main.core.models import TimeStampedModel
from main.yemekkalmasin_log.models import RequestLog


class UserLog(TimeStampedModel):
    class Meta:
        verbose_name = _('User Log')
        verbose_name_plural = _('User Logs')
        ordering = ('-created',)

    log_name        = models.CharField(max_length=300,blank=True, null=True, verbose_name=_('Log name'))
    request         = models.ForeignKey(RequestLog, blank=True, null=True, verbose_name=_('Request'), on_delete=models.SET_NULL)
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, verbose_name=_('User'), on_delete=models.SET_NULL)
    log_message     = models.TextField(blank=True, null=True, verbose_name=_('Log Message'))
    internel_name   = models.CharField(max_length=300,blank=True, null=True, verbose_name=_('Internal Event Name'))

    def save(self, *args, **kwargs):
        request = CrequestMiddleware.get_request()
        if not self.id:
            if request:
                v = RequestLog()
                v.from_http_request(request, None)
                self.request = v
            self.internel_name = str(self.log_name).replace(' ','_').lower()
        super(UserLog, self).save(*args, **kwargs)


    def __str__(self):
        return str(self.log_name)