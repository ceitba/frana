# coding: utf-8
from __future__ import unicode_literals
from datetime import date, timedelta

from constance import config
from django import forms
from django.contrib.auth.forms import AuthenticationForm as DjangoAuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import password_validators_help_text_html, validate_password
from django.core.exceptions import ValidationError
from django.db import transaction

from .fields import BootstrapDatepickerField
from .models import BookerProfile, Booking


class AuthenticationForm(DjangoAuthenticationForm):
    username = forms.EmailField(label="Email")


class EmailDomainValidator(object):
    domain = 'itba.edu.ar'

    def __call__(self, value):
        if not value.endswith(self.domain):
            raise ValidationError('Debes utilizar tu email @' + self.domain)



class SignupForm(forms.ModelForm):
    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label="Apellido(s)")
    email = forms.EmailField(
        label="Email",
        validators=[EmailDomainValidator()]
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(),
        help_text=password_validators_help_text_html(),
    )
    confirm_password = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(),
    )

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

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Este email ya se encuentra registrado.')
        return email

    def clean_password(self):
        password = self.cleaned_data['password']

        # create a temporary user to pass to validate_password
        user = User(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.data['email'],
        )
        validate_password(password, user)
        return password

    def clean_confirm_password(self):
        password = self.data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('Las contraseñas no coinciden.')
        return confirm_password

    def clean_license_expiration(self):
        expiration = self.cleaned_data['license_expiration']
        if expiration < date.today():
            raise ValidationError('El carnet está vencido.')
        return expiration

    @transaction.atomic
    def save(self, **kwargs):
        user = User(
            username=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
        )
        user.set_password(self.cleaned_data['password'])
        user.save()

        self.instance.user = user
        super(SignupForm, self).save(**kwargs)
        return user


class BookingForm(forms.Form):
    date = forms.DateField(label='Fecha')
    shift = forms.CharField(
        label='Turno',
        help_text='Los turnos son de <b>8 a 13</b> y de <b>13 a 18</b>.',
        widget=forms.RadioSelect(choices=Booking.SHIFT_CHOICES),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget = BootstrapDatepickerField(
            attrs={'required': 'required'},
            datepicker={
                'date-start-date': date.today().strftime('%d/%m/%Y'),
                'date-end-date': (date.today() + timedelta(days=config.BOOKING_DAYS_FUTURE)).strftime('%d/%m/%Y'),
            }
        )

    def clean(self):
        super(BookingForm, self).clean()

        date = self.cleaned_data.get('date', None)
        shift = self.cleaned_data.get('shift', None)

        if not date or not shift:
            return

        if date < date.today():
            raise ValidationError('La fecha elegida no es válida.')

        delta = config.BOOKING_DAYS_FUTURE
        if (date - date.today()).days > delta:
            msg = 'No puede reservar con más de {delta} días de anticipación.'
            raise ValidationError(msg.format(delta=delta))

        booking = Booking(
            date=date,
            shift=shift,
            user=self.user
        )
        booking.full_clean()

        profile = self.user.bookerprofile

        expiration = profile.license_expiration
        if expiration < self.cleaned_data['date']:
            msg = 'No podés hacer reservas con un carnet vencido.'
            raise ValidationError(msg)

        price = booking.get_price()
        if not profile.debit_credits and profile.credits < price:
            msg = 'No tenés créditos suficientes para reservar.'
            raise ValidationError(msg)

        self.booking = booking

    @transaction.atomic
    def save(self):
        profile = self.user.bookerprofile
        profile.credits -= self.booking.get_price()
        profile.save()
        self.booking.save()
        return self.booking
