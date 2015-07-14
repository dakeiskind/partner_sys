__author__ = 'wangwei'

from django.db import models


class Register(models.Model):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=60)
    email = models.EmailField()


class Contact(models.Model):
    name = models.CharField(max_length=40)
    title = models.CharField(max_length=40)
    tel = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    idCard = models.CharField(max_length=20)
    email = models.EmailField()
    idCopy = models.URLField()


class Potential(models.Model):
    zh_name = models.CharField(max_length=200)
    en_name = models.CharField(max_length=200)
    ceo = models.CharField(max_length=200)
    scope = models.CharField(max_length=200)
    founding = models.DateField()
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




