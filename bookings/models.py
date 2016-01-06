# coding: utf-8
from __future__ import unicode_literals
from datetime import date

from constance import config
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models, transaction


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
    credits = models.IntegerField(default=1000, verbose_name="Créditos")  # TODO: Change this once in production

    def __unicode__(self):
        return self.user.get_full_name()


class Booking(models.Model):
    SHIFT_CHOICES = (
        ('m', 'Mañana'),
        ('t', 'Tarde'),
    )

    STATUS_CHOICES = (
        ('c', 'Confirmada'),
        ('p', 'Pendiente'),
        ('x', 'Cancelada'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    date = models.DateField(verbose_name="Fecha")
    shift = models.CharField(
        max_length=1,
        choices=SHIFT_CHOICES,
        default='m',
        verbose_name="Turno")
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='c',
        verbose_name="Estado"
    )

    def __unicode__(self):
        return '{} a la {} por {}'.format(
            self.date, self.get_shift_display(), self.user)

    def clean(self):
        delta = config.BOOKING_DAYS_FUTURE
        if (self.date - date.today()).days > delta:
            msg = 'No puede reservar con más de {delta} días de anticipación.'
            raise ValidationError(msg.format(delta=delta))

        bookings_count = Booking.objects.filter(
            date=self.date,
            shift=self.shift,
            status='c'
        ).count()

        if bookings_count > 0:
            msg = 'Ya hay una reserva confirmada para esa fecha y turno.'
            raise ValidationError(msg)

    def get_price(self):
        if self.date.weekday() in [5, 6]:  # weekend
            return config.WEEKEND_PRICE
        else:
            return config.WEEKDAY_PRICE


class Credit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    comment = models.CharField(max_length=300)
