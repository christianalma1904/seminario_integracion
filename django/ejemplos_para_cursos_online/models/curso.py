from django.db import models
from .categoria_curso import CategoriaCurso

class Curso(models.Model):
    
    NIVEL_CHOICES = [
        ('principiante', 'Principiante'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
    ]
    
    categoria = models.ForeignKey(CategoriaCurso, on_delete=models.CASCADE, related_name="cursos")
    nombre = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_horas = models.PositiveIntegerField(help_text="Duracion total en horas")
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES, default='principiante')
    cupo_maximo = models.PositiveIntegerField(default=50, help_text="Numero maximo de estudiantes")
    activo = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("categoria", "nombre")
        ordering = ("-fecha_creacion",)
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

    def __str__(self):
        return self.nombre
    
    def estudiantes_inscritos(self):
        return self.inscripciones.filter(activa=True).count()
    
    def lugares_disponibles(self):
        return self.cupo_maximo - self.estudiantes_inscritos()
    
    def porcentaje_ocupacion(self):
        if self.cupo_maximo == 0:
            return 0
        return (self.estudiantes_inscritos() / self.cupo_maximo) * 100
    
    def precio_formateado(self):
        return f"${self.precio:,.2f}"