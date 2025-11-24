from django.db import models
from .estudiante import Estudiante
from .curso import Curso
from .leccion import Leccion

class Evaluacion(models.Model):
    
    TIPO_CHOICES = [
        ('quiz', 'Quiz'),
        ('examen', 'Examen'),
        ('proyecto', 'Proyecto'),
        ('participacion', 'Participacion'),
        ('final', 'Evaluacion Final'),
    ]
    
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name="evaluaciones")
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="evaluaciones")
    leccion = models.ForeignKey(Leccion, on_delete=models.CASCADE, null=True, blank=True, related_name="evaluaciones")
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    
    calificacion = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Calificacion obtenida")
    calificacion_maxima = models.DecimalField(max_digits=5, decimal_places=2, default=100, help_text="Calificacion maxima posible")
    
    completada = models.BooleanField(default=False)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    fecha_limite = models.DateTimeField(null=True, blank=True)
    
    comentarios_instructor = models.TextField(blank=True, help_text="Comentarios del instructor")
    comentarios_estudiante = models.TextField(blank=True, help_text="Comentarios del estudiante")
    
    archivo_entrega = models.URLField(blank=True, help_text="URL del archivo entregado por el estudiante")
    

    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha_asignacion"]
        verbose_name = "Evaluacion"
        verbose_name_plural = "Evaluaciones"

    def __str__(self):
        return f"{self.estudiante} - {self.curso.nombre} - {self.titulo}"
    
    def porcentaje_obtenido(self):
        if self.calificacion and self.calificacion_maxima:
            return (self.calificacion / self.calificacion_maxima) * 100
        return 0
    
    def esta_aprobada(self, nota_minima=70):
        return self.porcentaje_obtenido() >= nota_minima
    
    def esta_vencida(self):
        if not self.fecha_limite:
            return False
        
        from django.utils import timezone
        return timezone.now() > self.fecha_limite and not self.completada
    
    def dias_para_entrega(self):
        if not self.fecha_limite:
            return None
            
        from django.utils import timezone
        diferencia = self.fecha_limite - timezone.now()
        return diferencia.days if diferencia.days > 0 else 0
    
    def calificacion_formateada(self):
        if self.calificacion:
            return f"{self.calificacion}/{self.calificacion_maxima} ({self.porcentaje_obtenido():.1f}%)"
        return "Sin calificar"