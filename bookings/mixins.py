from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class AnonymousRequiredMixin(AccessMixin):
    redirect_url = 'bookings:index'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_anonymous():
            return self.handle_no_permission()
        return super(AnonymousRequiredMixin, self).dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return redirect(self.redirect_url)


class SuccessMessageMixin(object):

    success_message = None

    def get_success_message(self):
        if self.success_message:
            message = self.success_message
        else:
            raise ImproperlyConfigured(
                "No success message. Provide a success_message.")
        return message

    def form_valid(self, form):
        response = super(SuccessMessageMixin, self).form_valid(form)
        messages.success(self.request, self.get_success_message())
        return response
