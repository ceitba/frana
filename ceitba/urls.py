"""ceitba URL Configuration"""

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='bookings:index')),
    url(r'^bookings/', include('bookings.urls', namespace='bookings')),
    url(r'^admin/', admin.site.urls),
]
