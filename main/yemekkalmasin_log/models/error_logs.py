from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
import logging

from main.core.models import TimeStampedModel
from .request_log import RequestLog

class ErrorLog(TimeStampedModel):
    class Meta:
        verbose_name = _('Error Log')
        verbose_name_plural = _('Errors Logs')
        ordering = ('-created',)

    LOG_LEVELS = (
        (logging.NOTSET, _('NotSet')),
        (logging.INFO, _('Info')),
        (logging.WARNING, _('Warning')),
        (logging.DEBUG, _('Debug')),
        (logging.ERROR, _('Error')),
        (logging.FATAL, _('Fatal')),
    )

    logger_name = models.CharField(max_length=300,blank=True, null=True, verbose_name=_('logger name'))
    request = models.ForeignKey(RequestLog, blank=True, null=True, verbose_name=_('Request'), on_delete=models.SET_NULL)
    level = models.PositiveSmallIntegerField(choices=LOG_LEVELS, default=logging.ERROR, db_index=True)
    msg = models.TextField(blank=True, null=True, verbose_name=_('Error Message'))
    trace = models.TextField(blank=True, null=True, verbose_name=_('Error Trace'))

    def __str__(self):
        return str(self.msg)