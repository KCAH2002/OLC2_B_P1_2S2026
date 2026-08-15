from django.urls import path

from . import views


urlpatterns = [
    path("health/", views.health_check, name="health_check"), # ruta para la verifc de salud de la API
    path("analyze/", views.analyze_code, name="analyze_code"), # ruta para analizar el código OxigenScript
]