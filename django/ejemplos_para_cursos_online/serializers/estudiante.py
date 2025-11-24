from rest_framework import serializers
from django.contrib.auth.models import User
from ..models.estudiante import Estudiante

class EstudianteProfileSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.ReadOnlyField()
    email = serializers.ReadOnlyField()
    cursos_inscritos = serializers.ReadOnlyField()
    cursos_completados = serializers.ReadOnlyField()
    promedio_calificaciones = serializers.ReadOnlyField()
    
    class Meta:
        model = Estudiante
        fields = [
            'id',
            'nombre_completo',
            'email',
            'telefono',
            'fecha_nacimiento',
            'nivel_educativo',
            'biografia',
            'cursos_inscritos',
            'cursos_completados',
            'promedio_calificaciones',
            'fecha_registro'
        ]
        read_only_fields = ['fecha_registro']

class EstudianteSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    nombre_completo = serializers.ReadOnlyField()
    email = serializers.ReadOnlyField()
    cursos_inscritos = serializers.ReadOnlyField()
    cursos_completados = serializers.ReadOnlyField()
    promedio_calificaciones = serializers.ReadOnlyField()
    
    # Campos del usuario para escritura
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    email_usuario = serializers.EmailField(write_only=True, required=False, source='usuario.email')
    
    class Meta:
        model = Estudiante
        fields = [
            'id',
            'usuario',
            'nombre_completo',
            'email',
            'first_name',
            'last_name',
            'email_usuario',
            'telefono',
            'fecha_nacimiento',
            'nivel_educativo',
            'biografia',
            'cursos_inscritos',
            'cursos_completados',
            'promedio_calificaciones',
            'activo',
            'fecha_registro',
            'ultima_actividad'
        ]
        read_only_fields = ['fecha_registro', 'ultima_actividad']
        
    def update(self, instance, validated_data):
        # Actualizar datos del usuario si se proporcionan
        usuario_data = {}
        if 'first_name' in validated_data:
            usuario_data['first_name'] = validated_data.pop('first_name')
        if 'last_name' in validated_data:
            usuario_data['last_name'] = validated_data.pop('last_name')
        if 'usuario' in validated_data and 'email' in validated_data['usuario']:
            usuario_data['email'] = validated_data['usuario'].pop('email')
            
        if usuario_data:
            for attr, value in usuario_data.items():
                setattr(instance.usuario, attr, value)
            instance.usuario.save()
            
        # Actualizar el perfil del estudiante
        return super().update(instance, validated_data)