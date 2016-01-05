# coding: utf-8
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction

from .fields import BootstrapDatepickerField
from .models import BookerProfile, Booking


class SignupForm(forms.ModelForm):
    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label="Apellido(s)")
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirmar contraseña")

    class Meta:
        model = BookerProfile
        fields = [
            'first_name', 'last_name', 'email', 'password', 'confirm_password',
            'dni', 'student_file', 'license', 'license_expiration', 'address',
            'phone_number',
        ]
        widgets = {
            'license_expiration': BootstrapDatepickerField()
        }

    @transaction.atomic
    def save(self, **kwargs):
        user = User(
            username=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
        )
        user.set_password(self.cleaned_data['password']),
        user.save()

        self.instance.user = user
        return super(SignupForm, self).save(**kwargs)


class BookingForm(forms.Form):
    date = forms.DateField(
        label='Fecha',
        widget=BootstrapDatepickerField(),
    )
    shift = forms.CharField(
        label='Turno',
        widget=forms.RadioSelect(choices=Booking.SHIFT_CHOICES),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(BookingForm, self).__init__(*args, **kwargs)

    def clean(self):
        booking = Booking(
            date=self.cleaned_data['date'],
            shift=self.cleaned_data['shift'],
            user=self.user
        )
        booking.full_clean()

        price = booking.get_price()
        if self.user.bookerprofile.credits < price:
            msg = 'No tenés créditos suficientes para reservar.'
            raise ValidationError(msg)

        self.booking = booking

    @transaction.atomic
    def save(self):
        profile = self.user.bookerprofile
        profile.credits -= self.booking.get_price()
        profile.save()
        self.booking.save()
