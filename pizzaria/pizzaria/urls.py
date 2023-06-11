from django.contrib import admin
from django.urls import path
from Pizzaria_Mamma_Mia.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("login/", Login.as_view(), name="login"),
    path('admin/', admin.site.urls),
    path('cadastro/', cadastro, name="cadastrar"),
    path('store/', store),
] + static (settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
