from django.db import models
from django.contrib.auth.models import User

class Estudiante(models.Model):
    
    NIVEL_EDUCATIVO_CHOICES = [
        ('secundaria', 'Secundaria'),
        ('tecnico', 'Tecnico'),
        ('universitario', 'Universitario'),
        ('postgrado', 'Postgrado'),
        ('profesional', 'Profesional'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil_estudiante")
    telefono = models.CharField(max_length=15, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    nivel_educativo = models.CharField(max_length=20, choices=NIVEL_EDUCATIVO_CHOICES, blank=True)
    biografia = models.TextField(blank=True, help_text="Breve descripcion del estudiante")
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    ultima_actividad = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha_registro"]
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"

    def __str__(self):
        return f"{self.usuario.first_name} {self.usuario.last_name}" if self.usuario.first_name else self.usuario.username
    
    @property
    def nombre_completo(self):
        if self.usuario.first_name and self.usuario.last_name:
            return f"{self.usuario.first_name} {self.usuario.last_name}"
        return self.usuario.username
    
    @property
    def email(self):
        return self.usuario.email
    
    def cursos_inscritos(self):
        return self.inscripciones.filter(activa=True).count()
    
    def cursos_completados(self):
        return self.inscripciones.filter(activa=True, progreso=100).count()
    
    def promedio_calificaciones(self):
        evaluaciones = self.evaluaciones.filter(calificacion__isnull=False)
        if evaluaciones.exists():
            return evaluaciones.aggregate(models.Avg('calificacion'))['calificacion__avg']
        return None