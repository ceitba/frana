from django.conf.urls import url
import django.contrib.auth.views as auth_views
import django.contrib.flatpages.views as flatpages_views

from . import views
from .forms import AuthenticationForm
from .decorators import anonymous_required

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^login$', anonymous_required(auth_views.login),
        {'authentication_form': AuthenticationForm, 'template_name': 'bookings/login.html'}, name='login'),
    url(r'^logout$', auth_views.logout_then_login, name='logout'),
    url(r'^signup$', views.Signup.as_view(), name='signup'),
    url(r'^list$', views.Bookings.as_view(), name='bookings'),
    url(r'^(?P<pk>\d+)/cancel$', views.CancelBooking.as_view(), name='cancel'),
    url(r'^new$', views.Book.as_view(), name='book'),
    url(r'^contact$', views.Contact.as_view(), name='contact'),
    url(r'^privacy/', flatpages_views.flatpage, {'url': '/privacy/'}, name='privacy'),
    url(r'^terms/', flatpages_views.flatpage, {'url': '/terms/'}, name='terms'),
    url(r'^documents/', flatpages_views.flatpage, {'url': '/documents/'}, name='documents'),
]
