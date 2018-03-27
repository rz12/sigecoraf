from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from api.master import views
admin.autodiscover()
router = DefaultRouter(trailing_slash=False)

router.register(r'parametrizaciones', views.ParametrizacionViewSet, base_name='parametrizaciones')
urlpatterns = [
    url(r'^', include(router.urls)),
]
