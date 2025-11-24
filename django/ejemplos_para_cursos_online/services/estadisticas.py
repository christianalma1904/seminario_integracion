# Servicio para generar estadisticas de cursos
from django.db.models import Avg, Count, Q
from django.utils import timezone
from datetime import timedelta

class EstadisticasCursoService:
    
    @staticmethod
    def estadisticas_curso(curso):
        inscripciones = curso.inscripciones.filter(activa=True)
        
        return {
            'curso_id': curso.id,
            'nombre_curso': curso.nombre,
            'estudiantes_inscritos': inscripciones.count(),
            'estudiantes_activos': inscripciones.filter(estado__in=['en_curso', 'pagada']).count(),
            'estudiantes_completados': inscripciones.filter(estado='completada').count(),
            'promedio_progreso': inscripciones.aggregate(Avg('progreso'))['progreso__avg'] or 0,
            'promedio_calificaciones': inscripciones.exclude(calificacion_final__isnull=True).aggregate(Avg('calificacion_final'))['calificacion_final__avg'],
            'tasa_completacion': EstadisticasCursoService._calcular_tasa_completacion(inscripciones),
            'ocupacion_porcentaje': (inscripciones.count() / curso.cupo_maximo) * 100 if curso.cupo_maximo > 0 else 0
        }
    
    @staticmethod
    def estadisticas_estudiante(estudiante):
        inscripciones = estudiante.inscripciones.filter(activa=True)
        
        return {
            'estudiante_id': estudiante.id,
            'nombre_estudiante': estudiante.nombre_completo,
            'cursos_inscritos': inscripciones.count(),
            'cursos_en_progreso': inscripciones.filter(estado='en_curso').count(),
            'cursos_completados': inscripciones.filter(estado='completada').count(),
            'progreso_promedio': inscripciones.aggregate(Avg('progreso'))['progreso__avg'] or 0,
            'calificacion_promedio': estudiante.promedio_calificaciones(),
            'tiempo_estudiando': EstadisticasCursoService._calcular_tiempo_estudiando(estudiante),
            'certificados_obtenidos': inscripciones.filter(progreso=100, calificacion_final__gte=70).count()
        }
    
    @staticmethod
    def cursos_populares(limite=10):
        from ..models.curso import Curso
        
        return Curso.objects.annotate(
            total_inscripciones=Count('inscripciones', filter=Q(inscripciones__activa=True))
        ).filter(
            activo=True
        ).order_by('-total_inscripciones')[:limite]
    
    @staticmethod
    def estudiantes_activos(limite=10):
        from ..models.estudiante import Estudiante
        
        return Estudiante.objects.annotate(
            cursos_activos=Count('inscripciones', filter=Q(inscripciones__activa=True))
        ).filter(
            activo=True
        ).order_by('-cursos_activos')[:limite]
    
    @staticmethod
    def reporte_mensual():
        from ..models.inscripcion import Inscripcion
        from ..models.curso import Curso
        from ..models.estudiante import Estudiante
        
        inicio_mes = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        return {
            'periodo': inicio_mes.strftime('%B %Y'),
            'nuevas_inscripciones': Inscripcion.objects.filter(fecha_inscripcion__gte=inicio_mes).count(),
            'cursos_completados': Inscripcion.objects.filter(fecha_completado__gte=inicio_mes).count(),
            'nuevos_cursos': Curso.objects.filter(fecha_creacion__gte=inicio_mes).count(),
            'nuevos_estudiantes': Estudiante.objects.filter(fecha_registro__gte=inicio_mes).count(),
            'ingresos_estimados': EstadisticasCursoService._calcular_ingresos_mes(inicio_mes)
        }
    
    @staticmethod
    def _calcular_tasa_completacion(inscripciones):
        total = inscripciones.count()
        completados = inscripciones.filter(estado='completada').count()
        
        return (completados / total) * 100 if total > 0 else 0
    
    @staticmethod
    def _calcular_tiempo_estudiando(estudiante):
        primera_inscripcion = estudiante.inscripciones.order_by('fecha_inscripcion').first()
        if primera_inscripcion:
            dias = (timezone.now() - primera_inscripcion.fecha_inscripcion).days
            return f"{dias} dias"
        return "0 dias"
    
    @staticmethod
    def _calcular_ingresos_mes(inicio_mes):
        from ..models.inscripcion import Inscripcion
        
        inscripciones_mes = Inscripcion.objects.filter(
            fecha_inscripcion__gte=inicio_mes,
            estado__in=['pagada', 'en_curso', 'completada']
        ).select_related('curso')
        
        total = sum(inscripcion.curso.precio for inscripcion in inscripciones_mes)
        return float(total)