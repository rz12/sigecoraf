from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

admin.autodiscover()
router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    url(r'^', include(router.urls)),
     url(r'^api-token-auth/', views.obtain_auth_token),
]
