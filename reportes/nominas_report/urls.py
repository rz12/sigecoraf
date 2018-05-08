from django.conf.urls import url
from django.contrib import admin
from reportes.nominas_report import views

admin.autodiscover()

urlpatterns = [
    url(r'^rol-pago$', views.ver_rolpago,),
]
