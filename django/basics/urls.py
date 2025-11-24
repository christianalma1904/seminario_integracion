from django.urls import path
from . import views
urlpatterns = [
    path('area-triangulo/', views.area_triangulo, name='area_triangulo'),
    path('tabla-multiplicar/', views.tabla_multiplicar, name='tabla_multiplicar'),
    path('contar-mayores/', views.contar_mayores, name='contar_mayores'),
    path('sumar-consecutivos/', views.sumar_consecutivos, name='sumar_consecutivos'),
    path('calcular-promedio/', views.calcular_promedio, name='calcular_promedio'),
    path('potencia/', views.potencia, name='potencia'),


]