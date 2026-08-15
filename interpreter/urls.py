from django.urls import path

from . import views


urlpatterns = [
    path("health/", views.health_check, name="health_check"), # GET  /api/health/
    path("analyze/", views.analyze_code, name="analyze_code"), # POST /api/analyze/
]