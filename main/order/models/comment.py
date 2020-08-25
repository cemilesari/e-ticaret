from __future__ import unicode_literals
from django.db import models 
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from main.core.models import TimeStampedModel

from autoslug import AutoSlugField
from django.utils.text import slugify

from .product import Product
from main.users.models import User

class Comment(TimeStampedModel):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product")
    content = models.TextField()
    parent  = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    
    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.product.template.name + ' ' + self.user.username

    def save(self, *args, **kwargs):
        return super(Comment, self).save(*args, **kwargs)

    #bir yorumun reply var mı ? parentı ben olan yorumları bulmaya çalışıyor (dizi--cocuklar)
    def children(self):
        return Comment.objects.filter(parent=self)

    #exist varsa iç içe yani yorumun altında yorum var mı bunu ölçüyor  (var mı ?)
    @property
    def any_children(self):
        return Comment.objects.filter(parent= self).exists()    