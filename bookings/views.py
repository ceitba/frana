from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from .forms import SignupForm, BookingForm


class Index(TemplateView):
    template_name = 'bookings/index.html'


class Signup(TemplateView):
    from_class = SignupForm
    template_name = 'bookings/signup.html'
    success_url = reverse_lazy('bookings:thanks')


class SignupThanks(TemplateView):
    template_name = 'booking/signup_thanks.html'


class Login(FormView):
    form_class = AuthenticationForm
    template_name = 'bookings/login.html'
    success_url = reverse_lazy('bookings:index')


class Book(FormView):
    form = BookingForm
    template_name = 'bookings/form.html'
