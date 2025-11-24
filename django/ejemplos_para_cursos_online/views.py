# Mantiene las funciones basicas para retrocompatibilidad
# Las nuevas vistas CRUD estan en la carpeta views/

from .views.basicos import (
    calcular_area_aula,
    tabla_horarios, 
    contar_estudiantes_aprobados,
    calcular_duracion_curso,
    promedio_calificaciones_curso,
    calcular_progreso_estudiante
)