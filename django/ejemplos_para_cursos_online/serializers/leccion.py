from rest_framework import serializers
from ..models.leccion import Leccion

class LeccionBasicaSerializer(serializers.ModelSerializer):
    curso_nombre = serializers.CharField(source='curso.nombre', read_only=True)
    duracion_formateada = serializers.CharField(source='duracion_formateada', read_only=True)
    es_primera = serializers.BooleanField(read_only=True)
    es_ultima = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Leccion
        fields = [
            'id', 'titulo', 'orden', 'duracion_minutos', 'duracion_formateada',
            'tipo', 'curso_nombre', 'es_primera', 'es_ultima', 'activa'
        ]

class LeccionSerializer(serializers.ModelSerializer):
    duracion_formateada = serializers.CharField(source='duracion_formateada', read_only=True)
    es_primera = serializers.BooleanField(read_only=True)
    es_ultima = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Leccion
        fields = [
            'id', 'curso', 'titulo', 'descripcion', 'contenido',
            'orden', 'duracion_minutos', 'duracion_formateada', 'tipo',
            'url_video', 'url_material', 'es_primera', 'es_ultima', 
            'activa', 'fecha_creacion', 'fecha_actualizacion'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    def validate_orden(self, value):
        if value <= 0:
            raise serializers.ValidationError('El orden debe ser un número positivo')
        return value
    
    def validate_duracion_minutos(self, value):
        if value <= 0:
            raise serializers.ValidationError('La duración debe ser mayor a 0 minutos')
        if value > 480:  # 8 horas max
            raise serializers.ValidationError('La duración no puede ser mayor a 480 minutos (8 horas)')
        return value