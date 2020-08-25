from __future__ import unicode_literals, absolute_import
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from ..models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ("user","product", "content", "parent",)
	search_fields = list_display
	date_hierarchy = "created"
    