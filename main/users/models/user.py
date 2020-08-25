# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import ASCIIUsernameValidator, UnicodeUsernameValidator
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator, MinLengthValidator
from django.utils import six, timezone
from django.utils.text import slugify
from django.db import models
from django.db.models import Count, Q
from django.conf import settings
from django.core.cache import cache

from main.core.models import TimeStampedModel
from main.users.manager import UserManager

from autoslug import AutoSlugField
import pytz, os, random, pycountry

countries = sorted([(country.alpha_2, country.name) for country in pycountry.countries])

username_validator = UnicodeUsernameValidator() if six.PY3 else ASCIIUsernameValidator()
_PHONE_REGEX   = RegexValidator(regex=r'(\d{9,15})$', message=_("Your phone number should consist of 9-15 digits. Example: 1114442277"))

def get_random_pin():
	return random.choice(range(100000, 999999))

class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
	class Meta:
		verbose_name = _("User")
		verbose_name_plural = _("Users")
	CONSUMER = "consumer"
	RSLR_CLIENT = "reseller"
	RSLR_MANAGER = "reseller manager"
	ADMIN = "admin"
	ROLES = (
		(CONSUMER, _("Consumer"),),
		(RSLR_CLIENT, _("Reseller Client"),),
		(RSLR_MANAGER, _("Reseller Manager"),),
		(ADMIN, _("Administrator"),),
	)
	email 		= models.EmailField(_('Email address'), default="", unique=True, blank=True)
	pin 		= models.PositiveIntegerField(_("PIN"), default=get_random_pin, validators=[MinLengthValidator(6)],)
	full_name 	= models.CharField(_('Full name'), max_length=30, default="", blank=True)
	slug 		= AutoSlugField(populate_from='full_name', unique=True)
	birthdate 	= models.DateField(verbose_name=_("Birth Date"), null=True)
	is_staff 	= models.BooleanField(_('Is Staff'), default=False)
	is_active 	= models.BooleanField(_('Is Active'), default=False)
	is_email    = models.BooleanField(_('Is Email Verified'), default=False)
	role 		= models.CharField(verbose_name=_("Role"), max_length=15, choices=ROLES, default=CONSUMER)
	img 		= models.ImageField(verbose_name=_("Avatar"), upload_to=settings.DEFAULT_USER_FOLDER, blank=True, default=settings.DEFAULT_USER_AVATAR)
	city 		= models.CharField(verbose_name=_("City"), max_length=32, default=settings.DEFAULT_CITY_NAME)
	country     = models.CharField(verbose_name=_("Country"), max_length=2, default=settings.DEFAULT_COUNTRY_CODE)
	mob 		= models.CharField(verbose_name=_("Mobile"), max_length=15, blank=True, validators=[_PHONE_REGEX])
	push_notify = models.BooleanField(_('Push Notification'), default=True)
	newsletter  = models.BooleanField(_('Email Newsletter'), default=False)
	lati        = models.FloatField(_("Latitude"), default=0.0)
	lngt        = models.FloatField(_("Longitude"), default=0.0)
	terms       = models.BooleanField(_('Agree terms ') , default=False)
	username_validator = UnicodeUsernameValidator() if six.PY3 else ASCIIUsernameValidator()
	username 	= models.CharField(_('Username'), max_length=150, unique=True,
		help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
		validators=[username_validator],
		error_messages={
			'unique': _("A user with that username already exists."),
		},
	)

	objects = UserManager()
	EMAIL_FIELD = 'email'
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	@property
	def date_joined(self):
		return self.created
	def get_short_name(self):
		"Returns the short name for the user."
		return self.full_name if self.full_name else self.username
	get_short_name.short_description = _("Short Name")

	def save(self, *args, **kwargs):
		super(User, self).save(*args, **kwargs)
	def __str__(self):
		return self.full_name if self.full_name else self.username
	def get_dict(self):
		return {
			"pk": self.pk,
			"img": {"url": self.img.url, "name": self.img.name} if self.img else {"url": settings.DEFAULT_USER_AVATAR, "name": "user"},
			"username": self.username,
			"full_name": self.full_name,
			"email": self.email,
			"created": self.created.isoformat() if self.created else None,
		}