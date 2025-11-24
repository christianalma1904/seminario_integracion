from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from ..models.estudiante import Estudiante
from ..serializers.estudiante import EstudianteSerializer, EstudianteProfileSerializer

class EstudianteViewSet(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['nivel_educativo', 'activo']
    search_fields = ['usuario__first_name', 'usuario__last_name', 'usuario__email', 'biografia']
    ordering_fields = ['fecha_registro', 'ultima_actividad']
    ordering = ['-fecha_registro']

    def get_serializer_class(self):
        if self.action in ['list']:
            return EstudianteProfileSerializer
        return EstudianteSerializer

    @action(detail=True, methods=['get'])
    def perfil(self, request, pk=None):
        estudiante = self.get_object()
        serializer = EstudianteProfileSerializer(estudiante)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def cursos(self, request, pk=None):
        estudiante = self.get_object()
        inscripciones = estudiante.inscripciones.filter(activa=True)
        from ..serializers.inscripcion import InscripcionBasicaSerializer
        serializer = InscripcionBasicaSerializer(inscripciones, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def estadisticas(self, request, pk=None):
        estudiante = self.get_object()
        from ..services.estadisticas import EstadisticasCursoService
        stats = EstadisticasCursoService.estadisticas_estudiante(estudiante)
        return Response(stats)

    @action(detail=True, methods=['get'])
    def certificados(self, request, pk=None):
        estudiante = self.get_object()
        inscripciones_completadas = estudiante.inscripciones.filter(
            estado='completada',
            progreso=100
        )
        
        certificados = []
        for inscripcion in inscripciones_completadas:
            if inscripcion.puede_obtener_certificado():
                certificados.append({
                    'curso_id': inscripcion.curso.id,
                    'curso_nombre': inscripcion.curso.nombre,
                    'fecha_completado': inscripcion.fecha_fin,
                    'calificacion_final': inscripcion.calificacion_final,
                    'url_certificado': f'/api/cursos/certificados/{inscripcion.id}/'
                })
        
        return Response(certificados)

    @action(detail=False, methods=['get'])
    def activos(self, request):
        limite = int(request.query_params.get('limite', 10))
        from ..services.estadisticas import EstadisticasCursoService
        estudiantes = EstadisticasCursoService.estudiantes_activos(limite)
        serializer = EstudianteProfileSerializer(estudiantes, many=True)
        return Response(serializer.data)