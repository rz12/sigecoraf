from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from api.nominas import views

admin.autodiscover()
router = DefaultRouter(trailing_slash=False)

router.register(r'empleados', views.EmpleadoViewSet, base_name='empleados')
router.register(r'roles-pago', views.RolPagoViewSet, base_name='roles-pago')
router.register(r'cargos', views.CargoViewSet, base_name='cargos')
router.register(r'contratos', views.ContratoViewSet, base_name='contratos')

router.register(r'rolPago', views.CargoViewSet, base_name='rolPago')

urlpatterns = [
    url(r'^', include(router.urls)),
]
