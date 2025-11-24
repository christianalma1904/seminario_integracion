from rest_framework import serializers
from ..models.evaluacion import Evaluacion

class EvaluacionBasicaSerializer(serializers.ModelSerializer):
    estudiante_nombre = serializers.CharField(source='estudiante.nombre_completo', read_only=True)
    curso_nombre = serializers.CharField(source='curso.nombre', read_only=True)
    porcentaje_obtenido = serializers.FloatField(read_only=True)
    esta_aprobada = serializers.BooleanField(read_only=True)
    esta_vencida = serializers.BooleanField(read_only=True)
    dias_para_entrega = serializers.IntegerField(read_only=True)
    calificacion_formateada = serializers.CharField(read_only=True)
    
    class Meta:
        model = Evaluacion
        fields = [
            'id', 'titulo', 'tipo', 'estudiante_nombre', 'curso_nombre',
            'fecha_asignacion', 'fecha_limite', 'fecha_entrega', 
            'porcentaje_obtenido', 'esta_aprobada', 'esta_vencida',
            'dias_para_entrega', 'calificacion_formateada'
        ]

class EvaluacionSerializer(serializers.ModelSerializer):
    porcentaje_obtenido = serializers.FloatField(read_only=True)
    esta_aprobada = serializers.BooleanField(read_only=True)
    esta_vencida = serializers.BooleanField(read_only=True)
    dias_para_entrega = serializers.IntegerField(read_only=True)
    calificacion_formateada = serializers.CharField(read_only=True)
    
    class Meta:
        model = Evaluacion
        fields = [
            'id', 'estudiante', 'curso', 'titulo', 'descripcion', 'tipo', 
            'puntaje_maximo', 'nota_minima_aprobacion', 'fecha_asignacion', 
            'fecha_limite', 'fecha_entrega', 'fecha_calificacion',
            'respuesta_estudiante', 'calificacion', 'comentarios',
            'porcentaje_obtenido', 'esta_aprobada', 'esta_vencida', 
            'dias_para_entrega', 'calificacion_formateada'
        ]
        read_only_fields = ['fecha_asignacion', 'fecha_entrega', 'fecha_calificacion']
    
    def validate_puntaje_maximo(self, value):
        if value <= 0:
            raise serializers.ValidationError('El puntaje máximo debe ser mayor a 0')
        if value > 1000:
            raise serializers.ValidationError('El puntaje máximo no puede ser mayor a 1000')
        return value
    
    def validate_nota_minima_aprobacion(self, value):
        if value < 0:
            raise serializers.ValidationError('La nota mínima no puede ser negativa')
        return value
    
    def validate(self, attrs):
        puntaje_maximo = attrs.get('puntaje_maximo')
        nota_minima = attrs.get('nota_minima_aprobacion')
        fecha_limite = attrs.get('fecha_limite')
        
        if puntaje_maximo and nota_minima:
            if nota_minima > puntaje_maximo:
                raise serializers.ValidationError(
                    'La nota mínima de aprobación no puede ser mayor al puntaje máximo'
                )
        
        if fecha_limite:
            from django.utils import timezone
            if fecha_limite <= timezone.now():
                raise serializers.ValidationError(
                    'La fecha límite debe ser en el futuro'
                )
        
        return attrs