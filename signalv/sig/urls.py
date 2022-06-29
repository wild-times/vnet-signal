from django.urls import path

from . import views


app_name = "sig"


urlpatterns = [
    path('', views.home, name='home'),
]
