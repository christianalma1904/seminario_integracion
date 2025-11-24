from django.db import models
from .curso import Curso
from .estudiante import Estudiante

class Inscripcion(models.Model):
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente de Pago'),
        ('pagada', 'Pagada'),
        ('en_curso', 'En Curso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name="inscripciones")
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="inscripciones")
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    progreso = models.PositiveIntegerField(default=0, help_text="Porcentaje de progreso (0-100)")
    calificacion_final = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    fecha_completado = models.DateTimeField(null=True, blank=True)
    activa = models.BooleanField(default=True)
    notas_instructor = models.TextField(blank=True, help_text="Notas del instructor sobre el estudiante")
    
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("estudiante", "curso")
        ordering = ["-fecha_inscripcion"]
        verbose_name = "Inscripcion"
        verbose_name_plural = "Inscripciones"

    def __str__(self):
        return f"{self.estudiante} - {self.curso.nombre}"
    
    def porcentaje_progreso_formateado(self):
        return f"{self.progreso}%"
    
    def dias_inscrito(self):
        from django.utils import timezone
        return (timezone.now() - self.fecha_inscripcion).days
    
    def esta_aprobado(self, nota_minima=70):
        return self.calificacion_final and self.calificacion_final >= nota_minima
    
    def puede_obtener_certificado(self):
        return self.progreso == 100 and self.esta_aprobado()
    
    def tiempo_restante_estimado(self):
        if self.progreso == 0:
            return self.curso.duracion_horas
        
        tiempo_completado = (self.progreso / 100) * self.curso.duracion_horas
        return self.curso.duracion_horas - tiempo_completado