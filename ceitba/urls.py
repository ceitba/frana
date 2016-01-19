# coding: utf-8
"""ceitba URL Configuration"""

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView, RedirectView
import django.contrib.auth.views as auth_views

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='bookings:index')),
    url(r'^bookings/', include('bookings.urls', namespace='bookings')),
    url(r'^bookings/change-password$', auth_views.password_change,
        {'template_name': 'bookings/password_change.html'}, name='password_change'),
    url(r'^bookings/change-password/done$', auth_views.password_change_done,
        {'template_name': 'bookings/password_change_done.html'}, name='password_change_done'),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^404', TemplateView.as_view(template_name='404.html')),
        url(r'^500', TemplateView.as_view(template_name='500.html')),
        url(r'^400', TemplateView.as_view(template_name='400.html')),
        url(r'^403', TemplateView.as_view(template_name='403.html')),
    ]

admin.site.site_header = 'Administración de Reservas Frana'
