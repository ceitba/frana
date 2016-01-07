# coding: utf-8
from datetime import date

from constance import config
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView

from .emails import (
    SignupConfirmationEmail, BookingConfirmationEmail, BookingCancelledEmail
)
from .forms import SignupForm, BookingForm
from .mixins import AnonymousRequiredMixin, SuccessMessageMixin
from .models import Booking


class Index(TemplateView):
    template_name = 'bookings/index.html'

    def get_context_data(self, **kwargs):
        ctx = super(Index, self).get_context_data(**kwargs)
        ctx.update({
            'weekday_price': config.WEEKDAY_PRICE,
            'weekend_price': config.WEEKEND_PRICE,
        })

        if self.request.user.is_authenticated():
            expiration = self.request.user.bookerprofile.license_expiration
            expiration_delta = expiration - date.today()
            ctx['license_expiration'] = expiration_delta.days

        return ctx


class Signup(AnonymousRequiredMixin, SuccessMessageMixin, FormView):
    form_class = SignupForm
    template_name = 'bookings/signup.html'
    success_url = reverse_lazy('bookings:index')
    success_message = 'Gracias por registrarte. Pronto recibirás un email de confirmación.'

    def test_func(self):
        return self.request.user.is_anonymous()

    def form_valid(self, form):
        user = form.save()
        SignupConfirmationEmail(user).send()
        return super(Signup, self).form_valid(form)


class Bookings(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'bookings/bookings.html'

    def get_queryset(self):
        qs = super(Bookings, self).get_queryset()
        return qs.filter(date__gte=date.today()).prefetch_related('user')


class Book(SuccessMessageMixin, LoginRequiredMixin, FormView):
    form_class = BookingForm
    template_name = 'bookings/form.html'
    success_url = reverse_lazy('bookings:bookings')
    success_message = 'Gracias. Enseguida recibirás un email confirmando tu reserva.'

    def dispatch(self, request, *args, **kwargs):
        if config.BOOKING_DISABLED:
            messages.error(request, config.BOOKING_DISABLED_CAUSE)
            return redirect(request.META.get('HTTP_REFERER', 'bookings:index'))
        return super(Book, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(Book, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        booking = form.save()
        BookingConfirmationEmail(booking).send()
        return super(Book, self).form_valid(form)


class CancelBooking(LoginRequiredMixin, DetailView):
    model = Booking
    context_object_name = 'booking'
    template_name = 'bookings/cancel.html'

    def post(self, request, *args, **kwargs):
        booking = self.get_object()
        booking.status = 'x'
        booking.save()
        messages.success(request, 'La reserva fue cancelada.')
        BookingCancelledEmail(booking).send()
        return redirect('bookings:bookings')


class Contact(TemplateView):
    template_name = 'bookings/contact.html'
