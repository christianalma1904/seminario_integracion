from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count
from ..models.curso import Curso
from ..serializers.curso import CursoSerializer, CursoBasicoSerializer

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'nivel', 'activo']
    search_fields = ['nombre', 'descripcion', 'instructor']
    ordering_fields = ['nombre', 'precio', 'fecha_creacion', 'duracion_horas']
    ordering = ['-fecha_creacion']

    def get_serializer_class(self):
        if self.action in ['list']:
            return CursoBasicoSerializer
        return CursoSerializer

    @action(detail=True, methods=['get'])
    def estadisticas(self, request, pk=None):
        curso = self.get_object()
        from ..services.estadisticas import EstadisticasCursoService
        stats = EstadisticasCursoService.estadisticas_curso(curso)
        return Response(stats)

    @action(detail=True, methods=['get'])
    def inscripciones(self, request, pk=None):
        curso = self.get_object()
        inscripciones = curso.inscripciones.filter(activa=True)
        from ..serializers.inscripcion import InscripcionBasicaSerializer
        serializer = InscripcionBasicaSerializer(inscripciones, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def populares(self, request):
        limite = int(request.query_params.get('limite', 10))
        from ..services.estadisticas import EstadisticasCursoService
        cursos = EstadisticasCursoService.cursos_populares(limite)
        serializer = CursoBasicoSerializer(cursos, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def inscribir_estudiante(self, request, pk=None):
        curso = self.get_object()
        estudiante_id = request.data.get('estudiante_id')
        
        if not estudiante_id:
            return Response(
                {'error': 'estudiante_id es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from ..models.estudiante import Estudiante
            from ..models.inscripcion import Inscripcion
            
            estudiante = Estudiante.objects.get(id=estudiante_id)
            
            # Verificar si ya está inscrito
            if Inscripcion.objects.filter(
                estudiante=estudiante, 
                curso=curso, 
                activa=True
            ).exists():
                return Response(
                    {'error': 'El estudiante ya está inscrito en este curso'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Verificar cupo disponible
            if curso.cupo_maximo > 0:
                inscritos = curso.inscripciones.filter(activa=True).count()
                if inscritos >= curso.cupo_maximo:
                    return Response(
                        {'error': 'No hay cupos disponibles'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Crear inscripción
            inscripcion = Inscripcion.objects.create(
                estudiante=estudiante,
                curso=curso,
                estado='pagada'
            )
            
            from ..serializers.inscripcion import InscripcionSerializer
            serializer = InscripcionSerializer(inscripcion)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Estudiante.DoesNotExist:
            return Response(
                {'error': 'Estudiante no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )