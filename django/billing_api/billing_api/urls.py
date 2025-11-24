from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    # Las rutas de users y catalog se incluyen bajo el prefijo 'api/'
    path('api/', include('users.urls')),
    path('api/', include('catalog.urls')),
]