from __future__ import unicode_literals

from django.conf import settings
from django.db import models


class BookerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dni = models.CharField(max_length=10)
    license = models.CharField(max_length=16)
    birth_date = models.DateField()
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=16)
    student_file = models.PositiveIntegerField()
    credits = models.IntegerField()


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()


class Credit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    comment = models.CharField(max_length=300)
