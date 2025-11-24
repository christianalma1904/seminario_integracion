from rest_framework import serializers
from ..models.inscripcion import Inscripcion

class InscripcionBasicaSerializer(serializers.ModelSerializer):
    estudiante_nombre = serializers.CharField(source='estudiante.nombre_completo', read_only=True)
    curso_nombre = serializers.CharField(source='curso.nombre', read_only=True)
    progreso_formateado = serializers.CharField(source='progreso_formateado', read_only=True)
    dias_desde_inscripcion = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Inscripcion
        fields = [
            'id', 'estudiante_nombre', 'curso_nombre', 'estado', 'progreso',
            'progreso_formateado', 'calificacion_final', 'fecha_inscripcion',
            'dias_desde_inscripcion', 'activa'
        ]

class InscripcionSerializer(serializers.ModelSerializer):
    progreso_formateado = serializers.CharField(source='progreso_formateado', read_only=True)
    dias_desde_inscripcion = serializers.IntegerField(read_only=True)
    esta_aprobada = serializers.BooleanField(read_only=True)
    puede_obtener_certificado = serializers.BooleanField(read_only=True)
    tiempo_estimado_restante = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Inscripcion
        fields = [
            'id', 'estudiante', 'curso', 'estado', 'progreso', 'progreso_formateado', 
            'calificacion_final', 'fecha_inscripcion', 'fecha_inicio', 'fecha_fin', 
            'dias_desde_inscripcion', 'esta_aprobada', 'puede_obtener_certificado',
            'tiempo_estimado_restante', 'activa'
        ]
        read_only_fields = ['fecha_inscripcion']