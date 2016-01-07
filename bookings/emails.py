# coding: utf-8
from django.core.mail import EmailMessage
from django.template.loader import get_template


class TemplatedMessage(EmailMessage):
    template_name = None
    subject = None

    def __init__(self, **kwargs):
        kwargs.setdefault('subject', self.get_subject())
        kwargs.setdefault('body', self.get_body())
        super(TemplatedMessage, self).__init__(**kwargs)

    def get_context_data(self, **kwargs):
        return kwargs

    def get_subject(self):
        return self.subject

    def get_body(self):
        return get_template(self.template_name).render(self.get_context_data())


class SignupConfirmationEmail(TemplatedMessage):
    template_name = 'bookings/emails/signup_confirmation.txt'
    subject = '[CEITBA] Bienvenido a la web de reservas del Frana'

    def __init__(self, user):
        self.user = user
        super(SignupConfirmationEmail, self).__init__(
            to=[user.email]
        )

    def get_context_data(self, **kwargs):
        ctx = super(SignupConfirmationEmail, self).get_context_data(**kwargs)
        ctx['user'] = self.user
        return ctx


class BookingConfirmationEmail(TemplatedMessage):
    template_name = 'bookings/emails/booking_confirmation.txt'
    subject = '[CEITBA] Confirmación de reserva del Frana'

    def __init__(self, booking):
        self.booking = booking
        super(BookingConfirmationEmail, self).__init__(
            to=[booking.user.email]
        )

    def get_context_data(self, **kwargs):
        ctx = super(BookingConfirmationEmail, self).get_context_data(**kwargs)
        ctx['booking'] = self.booking
        return ctx


class BookingCancelledEmail(TemplatedMessage):
    template_name = 'bookings/emails/booking_cancelled.txt'
    subject = '[CEITBA] Reserva del Frana Cancelada'

    def __init__(self, booking):
        self.booking = booking
        super(BookingCancelledEmail, self).__init__(
            to=[booking.user.email]
        )

    def get_context_data(self, **kwargs):
        ctx = super(BookingCancelledEmail, self).get_context_data(**kwargs)
        ctx['booking'] = self.booking
        return ctx
