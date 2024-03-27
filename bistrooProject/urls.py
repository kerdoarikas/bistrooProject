from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("bistrooapp_admin/", include("bistrooapp_admin.urls")),
    path("", include("bistrooapp_public.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
]
