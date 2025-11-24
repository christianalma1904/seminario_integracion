from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from ..models.evaluacion import Evaluacion
from ..serializers.evaluacion import EvaluacionSerializer

class EvaluacionViewSet(viewsets.ModelViewSet):
    queryset = Evaluacion.objects.all()
    serializer_class = EvaluacionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo', 'curso', 'estudiante', 'aprobada']
    search_fields = ['titulo', 'descripcion']
    ordering_fields = ['fecha_asignacion', 'fecha_entrega', 'calificacion']
    ordering = ['-fecha_asignacion']

    @action(detail=True, methods=['post'])
    def calificar(self, request, pk=None):
        evaluacion = self.get_object()
        calificacion = request.data.get('calificacion')
        comentarios = request.data.get('comentarios', '')
        
        if calificacion is None:
            return Response(
                {'error': 'calificacion es requerida'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            calificacion = float(calificacion)
            if calificacion < 0 or calificacion > evaluacion.puntaje_maximo:
                return Response(
                    {'error': f'La calificación debe estar entre 0 y {evaluacion.puntaje_maximo}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            evaluacion.calificacion = calificacion
            evaluacion.comentarios = comentarios
            if not evaluacion.fecha_calificacion:
                from django.utils import timezone
                evaluacion.fecha_calificacion = timezone.now()
            
            evaluacion.save()
            
            serializer = self.get_serializer(evaluacion)
            return Response(serializer.data)
            
        except (ValueError, TypeError):
            return Response(
                {'error': 'La calificación debe ser un número válido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def entregar(self, request, pk=None):
        evaluacion = self.get_object()
        respuesta = request.data.get('respuesta', '')
        
        if not respuesta.strip():
            return Response(
                {'error': 'La respuesta no puede estar vacía'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if evaluacion.fecha_entrega:
            return Response(
                {'error': 'Esta evaluación ya ha sido entregada'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar si no está vencida
        if evaluacion.esta_vencida():
            return Response(
                {'error': 'El tiempo de entrega ha expirado'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        evaluacion.respuesta_estudiante = respuesta
        from django.utils import timezone
        evaluacion.fecha_entrega = timezone.now()
        evaluacion.save()
        
        serializer = self.get_serializer(evaluacion)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pendientes(self, request):
        estudiante_id = request.query_params.get('estudiante_id')
        if not estudiante_id:
            return Response(
                {'error': 'estudiante_id es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        evaluaciones = Evaluacion.objects.filter(
            estudiante_id=estudiante_id,
            fecha_entrega__isnull=True
        ).exclude(
            fecha_limite__lt=timezone.now()
        )
        
        serializer = self.get_serializer(evaluaciones, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def por_calificar(self, request):
        curso_id = request.query_params.get('curso_id')
        evaluaciones = Evaluacion.objects.filter(
            fecha_entrega__isnull=False,
            fecha_calificacion__isnull=True
        )
        
        if curso_id:
            evaluaciones = evaluaciones.filter(curso_id=curso_id)
        
        serializer = self.get_serializer(evaluaciones, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def estadisticas(self, request, pk=None):
        evaluacion = self.get_object()
        
        return Response({
            'titulo': evaluacion.titulo,
            'porcentaje_obtenido': evaluacion.porcentaje_obtenido(),
            'esta_aprobada': evaluacion.esta_aprobada(),
            'esta_vencida': evaluacion.esta_vencida(),
            'dias_para_entrega': evaluacion.dias_para_entrega(),
            'calificacion_formateada': evaluacion.calificacion_formateada()
        })