# coding: utf-8
"""ceitba URL Configuration"""

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
import django.contrib.auth.views as auth_views

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='bookings:index')),
    url(r'^bookings/', include('bookings.urls', namespace='bookings')),
    url(r'^bookings/change-password$', auth_views.password_change, {'template_name': 'bookings/password_change.html'}, name='password_change'),
    url(r'^bookings/change-password/done$', auth_views.password_change_done, {'template_name': 'bookings/password_change_done.html'}, name='password_change_done'),
    url(r'^admin/', admin.site.urls),
]

admin.site.site_header = 'Administración de Reservas Frana'
