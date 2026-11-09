from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sustentabilidad/', include('sustentabilidad.urls')),
]
