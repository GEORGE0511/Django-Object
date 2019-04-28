# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from django_web import models
admin.site.register(models.user)
admin.site.register(models.waterinfo)
admin.site.register(models.usewater)
admin.site.register(models.bill)
admin.site.register(models.employer)