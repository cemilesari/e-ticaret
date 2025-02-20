#example
from django.contrib.auth.models import User 
from django.db import models 
from django.db.models.signals import post_save 
from django.dispatch import receiver 


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    note = models.CharField(max_length=200)
    twitter = models.CharField(max_length = 200)



@receiver(post_save, sender= User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)
    instance.profile.save()
