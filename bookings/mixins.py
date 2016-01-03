from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages


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
