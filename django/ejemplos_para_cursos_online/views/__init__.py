# Inicializacion del modulo de vistas para cursos online
from .categoria_curso import CategoriaCursoViewSet
from .curso import CursoViewSet
from .estudiante import EstudianteViewSet
from .inscripcion import InscripcionViewSet
from .leccion import LeccionViewSet
from .evaluacion import EvaluacionViewSet
from .basicos import *

__all__ = [
    'CategoriaCursoViewSet',
    'CursoViewSet',
    'EstudianteViewSet', 
    'InscripcionViewSet',
    'LeccionViewSet',
    'EvaluacionViewSet',
    # Funciones basicas exportadas desde basicos.py
    'calcular_area_aula',
    'tabla_horarios',
    'contar_estudiantes_aprobados',
    'calcular_duracion_curso',
    'promedio_calificaciones_curso',
    'calcular_progreso_estudiante'
]