from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from ..models.leccion import Leccion
from ..serializers.leccion import LeccionSerializer

class LeccionViewSet(viewsets.ModelViewSet):
    queryset = Leccion.objects.all()
    serializer_class = LeccionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['curso', 'tipo_contenido', 'activa']
    search_fields = ['titulo', 'descripcion', 'contenido']
    ordering_fields = ['orden', 'duracion_minutos', 'fecha_creacion']
    ordering = ['curso', 'orden']

    def get_queryset(self):
        queryset = super().get_queryset()
        curso_id = self.request.query_params.get('curso')
        if curso_id:
            queryset = queryset.filter(curso_id=curso_id)
        return queryset

    @action(detail=True, methods=['get'])
    def anterior(self, request, pk=None):
        leccion = self.get_object()
        leccion_anterior = leccion.leccion_anterior()
        if leccion_anterior:
            serializer = self.get_serializer(leccion_anterior)
            return Response(serializer.data)
        else:
            return Response({'mensaje': 'Esta es la primera leccion del curso'})

    @action(detail=True, methods=['get'])
    def siguiente(self, request, pk=None):
        leccion = self.get_object()
        leccion_siguiente = leccion.leccion_siguiente()
        if leccion_siguiente:
            serializer = self.get_serializer(leccion_siguiente)
            return Response(serializer.data)
        else:
            return Response({'mensaje': 'Esta es la ultima leccion del curso'})

    @action(detail=True, methods=['post'])
    def marcar_completada(self, request, pk=None):
        leccion = self.get_object()
        estudiante_id = request.data.get('estudiante_id')
        
        if not estudiante_id:
            return Response(
                {'error': 'estudiante_id es requerido'}, 
                status=400
            )
        
        try:
            from ..models.estudiante import Estudiante
            estudiante = Estudiante.objects.get(id=estudiante_id)
            
            # Verificar que el estudiante está inscrito en el curso
            from ..models.inscripcion import Inscripcion
            try:
                inscripcion = Inscripcion.objects.get(
                    estudiante=estudiante,
                    curso=leccion.curso,
                    activa=True
                )
            except Inscripcion.DoesNotExist:
                return Response(
                    {'error': 'El estudiante no está inscrito en este curso'}, 
                    status=400
                )
            
            # Aquí podrías crear un modelo de progreso por lección
            # Por simplicidad, solo retornamos éxito
            
            return Response({
                'mensaje': f'Lección "{leccion.titulo}" marcada como completada',
                'estudiante': estudiante.nombre_completo,
                'leccion': leccion.titulo,
                'curso': leccion.curso.nombre
            })
            
        except Estudiante.DoesNotExist:
            return Response(
                {'error': 'Estudiante no encontrado'}, 
                status=404
            )

    @action(detail=False, methods=['get'])
    def por_curso(self, request):
        curso_id = request.query_params.get('curso_id')
        if not curso_id:
            return Response(
                {'error': 'curso_id es requerido'}, 
                status=400
            )
        
        lecciones = Leccion.objects.filter(
            curso_id=curso_id, 
            activa=True
        ).order_by('orden')
        
        serializer = self.get_serializer(lecciones, many=True)
        return Response(serializer.data)