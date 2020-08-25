from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from main.core.models import TimeStampedModel

class PasswordHistory(TimeStampedModel):
    class Meta:
        verbose_name = _("Password History")
        verbose_name_plural = _("Password Histories")
        ordering = ("-created",)
        
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True , on_delete=models.SET_NULL)
    user_password 	= models.CharField(_("User Password"), max_length=350,default='',unique=True)

    def get_dict(self):
        get_data = lambda obj: obj if obj else None
        return {
            'id':get_data(self.id),
            'user':get_data(self.user.id),
            'user_password':get_data(self.user_password),
        }

    def __str__(self):
        return self.user.username if self.user else "Deleted User"