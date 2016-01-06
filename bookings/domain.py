# coding: utf-8
from django.core.mail import EmailMessage
from django.template.loader import get_template


class TemplatedMessage(EmailMessage):
    template_name = None
    subject = None

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
            subject=self.get_subject(),
            body=self.get_body(),
            to=[user.email],
        )

    def get_context_data(self, **kwargs):
        ctx = super(SignupConfirmationEmail, self).get_context_data(**kwargs)
        ctx['user'] = self.user
        return ctx
