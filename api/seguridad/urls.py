from django.conf.urls import url, include
from django.contrib import admin
from api.seguridad import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as views_token

admin.autodiscover()
router = DefaultRouter(trailing_slash=False)

router.register(r'usuarios', views.UsuarioViewSet, base_name='usuarios')
router.register(r'menus', views.MenusViewSet, base_name='menus')
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-token-auth/', views_token.obtain_auth_token),
]
