# Importa todos los modelos desde la carpeta models
from .models.categoria_curso import CategoriaCurso
from .models.curso import Curso
from .models.estudiante import Estudiante
from .models.inscripcion import Inscripcion
from .models.leccion import Leccion
from .models.evaluacion import Evaluacion

# Mantiene retrocompatibilidad
__all__ = [
    'CategoriaCurso',
    'Curso', 
    'Estudiante',
    'Inscripcion',
    'Leccion',
    'Evaluacion'
]