from django.contrib import admin
from django.urls import path
from Pizzaria_Mamma_Mia.views import *

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path('admin/', admin.site.urls),
]
