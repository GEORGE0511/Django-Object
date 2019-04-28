# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models
class user(models.Model):
    id=models.CharField(max_length=20,primary_key=True)
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=32)
    balance=models.DecimalField(max_digits=11,decimal_places=2,default=0.00)
    email=models.CharField(max_length=32)
class waterinfo(models.Model):
    wid=models.CharField(max_length=20,primary_key=True)
    wname=models.CharField(max_length=100,null=False)
    price=models.DecimalField(max_digits=11,decimal_places=2)
class usewater(models.Model):
    num=models.CharField(max_length=12,primary_key=True)
    id = models.ForeignKey('User')
    umonth=models.CharField(max_length=6)
    flag=models.CharField(max_length=20,default='未达')
    flag2 = models.CharField(max_length=20, default=0)
    wid=models.ForeignKey('waterinfo')
    water_c=models.IntegerField(max_length=32)
    ymoney=models.DecimalField(max_digits=11,decimal_places=2)
class employer(models.Model):
    eid=models.CharField(max_length=20,primary_key=True)
    ename=models.CharField(max_length=100)
    esex=models.CharField(max_length=10)
    ekey=models.CharField(max_length=32)
    ephone = models.CharField(max_length=50)
class bill(models.Model):
    num=models.ForeignKey('usewater')
    eid=models.ForeignKey('employer')