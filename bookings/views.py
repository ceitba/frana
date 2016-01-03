# coding: utf-8
from constance import config
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from .mixins import SuccessMessageMixin
from .forms import SignupForm, BookingForm


class Index(TemplateView):
    template_name = 'bookings/index.html'

    def get_context_data(self, **kwargs):
        ctx = super(Index, self).get_context_data(**kwargs)
        ctx.update({
            'weekday_price': config.WEEKDAY_PRICE,
            'weekend_price': config.WEEKEND_PRICE,
        })
        return ctx


class Signup(SuccessMessageMixin, FormView):
    form_class = SignupForm
    template_name = 'bookings/signup.html'
    success_url = reverse_lazy('bookings:index')
    success_message = 'Gracias por registrarte. Pronto recibirás un email de confirmación.'

    def form_valid(self, form):
        form.save()
        return super(Signup, self).form_valid(form)


class Login(FormView):
    form_class = AuthenticationForm
    template_name = 'bookings/login.html'
    success_url = reverse_lazy('bookings:index')


class Book(LoginRequiredMixin, FormView):
    form_class = BookingForm
    template_name = 'bookings/form.html'


class Contact(TemplateView):
    template_name = 'bookings/contact.html'
