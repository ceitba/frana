# coding: utf-8
from __future__ import unicode_literals

from constance import config
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django_extensions.db.models import TimeStampedModel


class Holiday(models.Model):
    description = models.CharField(max_length=90, verbose_name="Descripción")
    date = models.DateField(unique=True)

    class Meta:
        verbose_name = "Feriado"

    def __unicode__(self):
        return unicode(self.date)


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
    debit_credits = models.BooleanField(default=False, verbose_name="Debitar créditos")

    class Meta:
        verbose_name = "Navegante"

    def __unicode__(self):
        return self.user.get_full_name()


class Booking(TimeStampedModel):
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

    class Meta:
        verbose_name = "Reserva"

    def __unicode__(self):
        return '{} a la {} por {}'.format(
            self.date, self.get_shift_display(), self.user)

    def clean(self):
        bookings_count = Booking.objects.filter(
            date=self.date,
            shift=self.shift,
            status='c'
        ).count()

        if bookings_count > 0:
            msg = 'Ya hay una reserva confirmada para esa fecha y turno.'
            raise ValidationError(msg)

    def _is_holiday(self, date):
        return Holiday.objects.filter(date=date).exists()

    def get_price(self):
        if self._is_holiday(self.date) or self.date.weekday() in [5, 6]:  # weekend
            return config.WEEKEND_PRICE
        else:
            return config.WEEKDAY_PRICE


class Credit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    comment = models.CharField(max_length=300)

    class Meta:
        verbose_name = "Crédito"

    def __unicode__(self):
        return '{} for {}'.format(self.amount, self.user)
