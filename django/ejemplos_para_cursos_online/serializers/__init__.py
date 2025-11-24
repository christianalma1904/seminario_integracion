# Inicializacion del modulo de serializers para cursos online
from .categoria_curso import CategoriaCursoSerializer
from .curso import CursoSerializer, CursoBasicoSerializer
from .estudiante import EstudianteSerializer, EstudianteProfileSerializer
from .inscripcion import InscripcionSerializer, InscripcionBasicaSerializer
from .leccion import LeccionSerializer, LeccionBasicaSerializer
from .evaluacion import EvaluacionSerializer, EvaluacionBasicaSerializer

__all__ = [
    'CategoriaCursoSerializer',
    'CursoSerializer',
    'CursoBasicoSerializer', 
    'EstudianteSerializer',
    'EstudianteProfileSerializer',
    'InscripcionSerializer',
    'InscripcionBasicaSerializer',
    'LeccionSerializer', 
    'LeccionBasicaSerializer',
    'EvaluacionSerializer',
    'EvaluacionBasicaSerializer',
]