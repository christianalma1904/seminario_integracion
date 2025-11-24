from django.contrib import admin
from .models.categoria_curso import CategoriaCurso
from .models.curso import Curso
from .models.estudiante import Estudiante
from .models.inscripcion import Inscripcion
from .models.leccion import Leccion
from .models.evaluacion import Evaluacion

@admin.register(CategoriaCurso)
class CategoriaCursoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activa', 'fecha_creacion']
    list_filter = ['activa', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    ordering = ['nombre']
    prepopulated_fields = {'slug': ('nombre',)}

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'duracion_horas', 'activo', 'fecha_creacion']
    list_filter = ['categoria', 'activo', 'nivel', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion', 'instructor']
    ordering = ['-fecha_creacion']
    prepopulated_fields = {'slug': ('nombre',)}

@admin.register(Estudiante) 
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'email', 'nivel_educativo', 'activo', 'fecha_registro']
    list_filter = ['activo', 'nivel_educativo', 'fecha_registro']
    search_fields = ['usuario__first_name', 'usuario__last_name', 'usuario__email', 'biografia']
    ordering = ['-fecha_registro']

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'curso', 'estado', 'progreso', 'calificacion_final', 'fecha_inscripcion']
    list_filter = ['estado', 'activa', 'fecha_inscripcion', 'curso__categoria']
    search_fields = ['estudiante__usuario__first_name', 'estudiante__usuario__last_name', 'curso__nombre']
    ordering = ['-fecha_inscripcion']

@admin.register(Leccion)
class LeccionAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'curso', 'orden', 'duracion_minutos', 'tipo', 'activa']
    list_filter = ['curso', 'tipo', 'activa', 'fecha_creacion']
    search_fields = ['titulo', 'descripcion', 'contenido']
    ordering = ['curso', 'orden']

@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'estudiante', 'curso', 'tipo', 'calificacion', 'esta_aprobada', 'fecha_asignacion']
    list_filter = ['tipo', 'curso', 'fecha_asignacion']
    search_fields = ['titulo', 'estudiante__usuario__first_name', 'estudiante__usuario__last_name', 'curso__nombre']
    ordering = ['-fecha_asignacion']