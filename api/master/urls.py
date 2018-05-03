from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from api.master import views
admin.autodiscover()
router = DefaultRouter(trailing_slash=False)

router.register(r'parametrizaciones', views.ParametrizacionViewSet, base_name='parametrizaciones')
router.register(r'empresas', views.EmpresaViewSet, base_name='empresas')
router.register(r'catalogos', views.CatalogoViewSet, base_name='catalogos')
router.register(r'direcciones', views.DireccionViewSet, base_name='direcciones')
router.register(r'items', views.ItemViewSet, base_name='items')
urlpatterns = [
    url(r'^', include(router.urls)),
]
