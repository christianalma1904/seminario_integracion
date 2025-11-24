from rest_framework import serializers
from ..models.curso import Curso
from .categoria_curso import CategoriaCursoSerializer

class CursoBasicoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    estudiantes_inscritos = serializers.ReadOnlyField()
    lugares_disponibles = serializers.ReadOnlyField()
    porcentaje_ocupacion = serializers.ReadOnlyField()
    precio_formateado = serializers.ReadOnlyField()
    
    class Meta:
        model = Curso
        fields = [
            'id', 'nombre', 'slug', 'categoria_nombre', 'precio', 'precio_formateado',
            'nivel', 'duracion_horas', 'cupo_maximo', 'estudiantes_inscritos',
            'lugares_disponibles', 'porcentaje_ocupacion', 'activo', 'fecha_creacion'
        ]

class CursoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Curso
        fields = [
            'id', 'nombre', 'slug', 'descripcion', 'categoria',
            'precio', 'duracion_horas', 'nivel', 'cupo_maximo',
            'activo', 'destacado', 'fecha_inicio', 'fecha_fin',
            'fecha_creacion', 'fecha_actualizacion'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']
        
    def validate_cupo_maximo(self, value):
        if value <= 0:
            raise serializers.ValidationError("El cupo maximo debe ser mayor a cero")
        return value
        
    def validate_duracion_horas(self, value):
        if value <= 0:
            raise serializers.ValidationError("La duracion debe ser mayor a cero")
        return value
        
    def validate(self, data):
        if data.get('fecha_inicio') and data.get('fecha_fin'):
            if data['fecha_fin'] <= data['fecha_inicio']:
                raise serializers.ValidationError("La fecha fin debe ser posterior a la fecha inicio")
        return data