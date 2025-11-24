from django.db import models
from .curso import Curso

class Leccion(models.Model):
    
    TIPO_CHOICES = [
        ('video', 'Video'),
        ('texto', 'Texto'),
        ('pdf', 'PDF'),
        ('quiz', 'Quiz'),
        ('proyecto', 'Proyecto'),
        ('discusion', 'Discusion'),
    ]
    
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='lecciones')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    contenido = models.TextField(blank=True, help_text="Contenido de la leccion")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='video')
    duracion_minutos = models.PositiveIntegerField(help_text="Duracion estimada en minutos")
    orden = models.PositiveIntegerField(help_text="Orden de la leccion en el curso")
    es_gratuita = models.BooleanField(default=False, help_text="Si la leccion es de vista previa gratuita")
    activa = models.BooleanField(default=True)
    
    url_video = models.URLField(blank=True, help_text="URL del video si aplica")
    url_archivo = models.URLField(blank=True, help_text="URL del archivo descargable si aplica")
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("curso", "orden")
        ordering = ["curso", "orden"]
        verbose_name = "Leccion"
        verbose_name_plural = "Lecciones"

    def __str__(self):
        return f"{self.curso.nombre} - Leccion {self.orden}: {self.titulo}"
    
    def duracion_formateada(self):
        horas = self.duracion_minutos // 60
        minutos = self.duracion_minutos % 60
        
        if horas > 0:
            return f"{horas}h {minutos}m"
        return f"{minutos}m"
    
    def es_la_primera(self):
        return self.orden == 1
    
    def es_la_ultima(self):
        return self.orden == self.curso.lecciones.filter(activa=True).count()
    
    def leccion_anterior(self):
        return self.curso.lecciones.filter(orden__lt=self.orden, activa=True).last()
    
    def leccion_siguiente(self):
        return self.curso.lecciones.filter(orden__gt=self.orden, activa=True).first()
    
    def completada_por_estudiante(self, estudiante):
        return False