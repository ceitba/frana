# coding: utf-8
from django import forms
from django.contrib.auth.models import User
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


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ['user', 'pending']
        widgets = {
            'date': BootstrapDatepickerField()
        }

    def clean_date(self, value):
        import pdb; pdb.set_trace()
        pass
