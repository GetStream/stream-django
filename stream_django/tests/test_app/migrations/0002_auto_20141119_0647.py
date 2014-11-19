# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_a_user(apps, schema_editor):
    User = apps.get_model("auth", "User")
    User.objects.create(username='segundo')


def create_a_pin(apps, schema_editor):
    User = apps.get_model("auth", "User")
    Pin = apps.get_model("test_app", "Pin")
    Pin.objects.create(author=User.objects.first())


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_a_user),
        migrations.RunPython(create_a_pin),
    ]
