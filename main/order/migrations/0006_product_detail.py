# Generated by Django 2.2.7 on 2020-08-25 09:06

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_auto_20200825_0843'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='detail',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
    ]
