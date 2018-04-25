from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from api.nominas import views

admin.autodiscover()
router = DefaultRouter(trailing_slash=False)

router.register(r'empleados', views.EmpleadoViewSet, base_name='empleados')
router.register(r'cargos', views.CargoViewSet, base_name='cargos')
router.register(r'contratos', views.ContratoViewSet, base_name='contratos')
router.register(r'consolidado-rolpago', views.ConsolidadoRolPagoViewSet, base_name='consolidado-rolpago')

router.register(r'rol-pago', views.RolPagoViewSet, base_name='rol-pago')

urlpatterns = [
    url(r'^', include(router.urls)),
]
