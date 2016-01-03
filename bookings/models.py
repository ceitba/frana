# coding: utf-8
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from model_utils import Choices


class BookerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    dni = models.CharField(max_length=10, verbose_name="DNI")
    license = models.CharField(max_length=16, verbose_name="Carnet")
    license_expiration = models.DateField(verbose_name="Fecha de vencimiento")
    address = models.CharField(max_length=200, verbose_name="Dirección")
    phone_number = models.CharField(max_length=16, verbose_name="Teléfono")
    student_file = models.PositiveIntegerField(verbose_name="Legajo")
    credits = models.IntegerField(default=0, verbose_name="Créditos")

    def __unicode__(self):
        return self.user.get_full_name()


class Booking(models.Model):
    SHIFT_CHOICES = (
        ('m', 'Mañana'),
        ('t', 'Tarde'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    date = models.DateTimeField(verbose_name="Fecha")
    shift = models.CharField(
        max_length=1,
        choices=SHIFT_CHOICES,
        verbose_name="Turno")

    def __unicode__(self):
        return '{} a la {} por {}'.format(
            self.date, self.get_shift_display(), self.user)


class Credit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    comment = models.CharField(max_length=300)
