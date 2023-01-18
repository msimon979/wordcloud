from django.contrib import admin
from django.urls import path

from clouds.views import SubmitUrlView, WordsView

# from rest_framework.authtoken.views import obtain_auth_token
# from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("clouds/submit/", SubmitUrlView.as_view(), name="submit_url"),
    path("clouds/top-words/", WordsView.as_view(), name="get_words"),
]
