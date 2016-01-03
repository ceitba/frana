from django.contrib import admin

from .models import BookerProfile, Booking

admin.site.register(BookerProfile)
admin.site.register(Booking)
