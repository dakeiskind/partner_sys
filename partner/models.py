__author__ = 'wangwei'

from django.db import models
from decimal import *
import datetime


class Register(models.Model):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=60)
    email = models.EmailField()

    def tojson(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        d = {}
        for attr in fields:
            if isinstance(getattr(self, attr), datetime.datetime):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr), datetime.date):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            else:
                d[attr] = getattr(self, attr)

        return d


class Contact(models.Model):
    name = models.CharField(max_length=40)
    title = models.CharField(max_length=40)
    tel = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    idCard = models.CharField(max_length=20)
    email = models.EmailField()
    idCopy = models.URLField()

    def tojson(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        d = {}
        for attr in fields:
            if isinstance(getattr(self, attr), datetime.datetime):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr), datetime.date):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            else:
                d[attr] = getattr(self, attr)

        return d


class Potential(models.Model):
    zh_name = models.CharField(max_length=200)
    en_name = models.CharField(max_length=200)
    ceo = models.CharField(max_length=200)
    scope = models.CharField(max_length=200)
    founding = models.DateTimeField()
    capital = models.DecimalField(max_digits=20, decimal_places=2)
    licence = models.CharField(max_length=80)
    licenceCopy = models.URLField()
    tax = models.CharField(max_length=80)
    taxCopy = models.URLField()
    orgCode = models.CharField(max_length=80)
    orgCodeCopy = models.URLField()
    employees = models.IntegerField()
    address = models.CharField(max_length=200)
    homepage = models.URLField()
    tel = models.CharField(max_length=20)
    fax = models.CharField(max_length=20)
    email = models.EmailField()
    summary = models.TextField()
    cases = models.TextField()
    register = models.ForeignKey(Register)
    contact = models.ForeignKey(Contact)

    def tojson(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        d = {}
        for attr in fields:
            if isinstance(getattr(self, attr), datetime.datetime):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr), datetime.date):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            elif isinstance(getattr(self, attr), Register):
                d['register'] = getattr(self, attr).tojson()
            elif isinstance(getattr(self, attr), Contact):
                d['contact'] = getattr(self, attr).tojson()
            elif isinstance(getattr(self, attr), Decimal):
                d[attr] = str(getattr(self, attr))
            else:
                d[attr] = getattr(self, attr)

        return d


#class SB(models.Model):
#    create = models.DateTimeField()
