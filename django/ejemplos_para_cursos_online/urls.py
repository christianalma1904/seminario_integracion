from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    CategoriaCursoViewSet, 
    CursoViewSet,
    EstudianteViewSet,
    InscripcionViewSet,
    LeccionViewSet,
    EvaluacionViewSet
)

# Router para ViewSets
router = DefaultRouter()
router.register(r'categorias', CategoriaCursoViewSet)
router.register(r'cursos', CursoViewSet) 
router.register(r'estudiantes', EstudianteViewSet)
router.register(r'inscripciones', InscripcionViewSet)
router.register(r'lecciones', LeccionViewSet)
router.register(r'evaluaciones', EvaluacionViewSet)

urlpatterns = [
    # APIs CRUD con ViewSets
    path('', include(router.urls)),
    
    # Funciones básicas (sin ViewSets)
    path('calcular-area-aula/', views.calcular_area_aula, name='calcular_area_aula'),
    path('tabla-horarios/', views.tabla_horarios, name='tabla_horarios'),
    path('contar-estudiantes-aprobados/', views.contar_estudiantes_aprobados, name='contar_estudiantes_aprobados'),
    path('promedio-calificaciones/', views.promedio_calificaciones_curso, name='promedio_calificaciones_curso'),
    path('calcular-duracion-curso/', views.calcular_duracion_curso, name='calcular_duracion_curso'),
    path('calcular-progreso-estudiante/', views.calcular_progreso_estudiante, name='calcular_progreso_estudiante'),
]