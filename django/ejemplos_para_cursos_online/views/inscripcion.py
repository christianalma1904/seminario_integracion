from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from ..models.inscripcion import Inscripcion
from ..serializers.inscripcion import InscripcionSerializer

class InscripcionViewSet(viewsets.ModelViewSet):
    queryset = Inscripcion.objects.all()
    serializer_class = InscripcionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['estado', 'activa', 'curso', 'estudiante']
    search_fields = ['curso__nombre', 'estudiante__usuario__first_name', 'estudiante__usuario__last_name']
    ordering_fields = ['fecha_inscripcion', 'fecha_inicio', 'progreso']
    ordering = ['-fecha_inscripcion']

    @action(detail=True, methods=['post'])
    def actualizar_progreso(self, request, pk=None):
        inscripcion = self.get_object()
        progreso = request.data.get('progreso')
        
        if progreso is None:
            return Response(
                {'error': 'progreso es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            progreso = float(progreso)
            if progreso < 0 or progreso > 100:
                return Response(
                    {'error': 'El progreso debe estar entre 0 y 100'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            inscripcion.progreso = progreso
            
            # Si completa el curso, actualizar estado
            if progreso == 100:
                inscripcion.estado = 'completada'
                if not inscripcion.fecha_fin:
                    from django.utils import timezone
                    inscripcion.fecha_fin = timezone.now()
            
            inscripcion.save()
            
            serializer = self.get_serializer(inscripcion)
            return Response(serializer.data)
            
        except (ValueError, TypeError):
            return Response(
                {'error': 'El progreso debe ser un número válido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def calificar(self, request, pk=None):
        inscripcion = self.get_object()
        calificacion = request.data.get('calificacion_final')
        
        if calificacion is None:
            return Response(
                {'error': 'calificacion_final es requerida'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            calificacion = float(calificacion)
            if calificacion < 0 or calificacion > 100:
                return Response(
                    {'error': 'La calificación debe estar entre 0 y 100'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            inscripcion.calificacion_final = calificacion
            inscripcion.save()
            
            serializer = self.get_serializer(inscripcion)
            return Response(serializer.data)
            
        except (ValueError, TypeError):
            return Response(
                {'error': 'La calificación debe ser un número válido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['get'])
    def tiempo_restante(self, request, pk=None):
        inscripcion = self.get_object()
        tiempo_estimado = inscripcion.tiempo_estimado_restante()
        
        return Response({
            'tiempo_estimado_dias': tiempo_estimado,
            'progreso_actual': inscripcion.progreso,
            'dias_desde_inicio': inscripcion.dias_desde_inscripcion()
        })

    @action(detail=False, methods=['get'])
    def reporte_mensual(self, request):
        anio = int(request.query_params.get('anio', 2025))
        mes = int(request.query_params.get('mes', 11))
        
        from ..services.estadisticas import EstadisticasCursoService
        reporte = EstadisticasCursoService.reporte_mensual(anio, mes)
        return Response(reporte)