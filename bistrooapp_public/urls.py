from django.urls import path
from . import views

app_name = "bistrooapp_public"


urlpatterns = [
    path("", views.show_menu, name="index"),
]