from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from api.nominas import views

admin.autodiscover()
router = DefaultRouter(trailing_slash=False)

router.register(r'empleados', views.EmpleadoViewSet, base_name='empleados')

urlpatterns = [
    url(r'^', include(router.urls)),
]
