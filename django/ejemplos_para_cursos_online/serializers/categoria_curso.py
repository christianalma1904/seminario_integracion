from rest_framework import serializers
from ..models.categoria_curso import CategoriaCurso

class CategoriaCursoSerializer(serializers.ModelSerializer):
    cantidad_cursos = serializers.ReadOnlyField()
    
    class Meta:
        model = CategoriaCurso
        fields = [
            'id',
            'nombre',
            'slug', 
            'descripcion',
            'activa',
            'cantidad_cursos',
            'fecha_creacion',
            'fecha_actualizacion'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']