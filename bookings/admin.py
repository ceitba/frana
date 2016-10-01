# coding: utf-8
from functools import update_wrapper

from django.conf.urls import url
from django.contrib import admin, messages
from django.shortcuts import redirect

from .models import BookerProfile, Booking, Holiday
from .service import HolidayUpdater


class HolidayAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super(HolidayAdmin, self).get_urls()

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        return [
            url(r'^update_all/$', wrap(update_holidays), name='bookings_holiday_update'),
        ] + urls


def update_holidays(request):
    try:
        added = HolidayUpdater().update()
        if added == 0:
            message = "No se encontraron feriados nuevos."
        elif added == 1:
            message = "Se añadió un feriado nuevo."
        else:
            message = "Se añadieron {} feriados nuevos.".format(added)
        messages.success(request, message)

    except HolidayUpdater.ConnectionError:
        messages.error(request,
            "No se pudo actualizar la lista de feriados. La fuente no está disponible en este momento.")

    return redirect('admin:bookings_holiday_changelist')


admin.site.register(BookerProfile)
admin.site.register(Booking)
admin.site.register(Holiday, HolidayAdmin)
