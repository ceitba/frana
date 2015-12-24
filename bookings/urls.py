from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^login$', views.Login.as_view(), name='login'),
    url(r'^signup$', views.Signup.as_view(), name='signup'),
    url(r'^new$', views.Book.as_view(), name='book'),
]
