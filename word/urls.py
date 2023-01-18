from django.contrib import admin
from django.urls import include, path

# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("admin/", admin.site.urls)
]
