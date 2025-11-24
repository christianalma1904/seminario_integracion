from django.db import models

class CategoriaCurso(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("nombre",)
        verbose_name = "Categoria de Curso"
        verbose_name_plural = "Categorias de Cursos"

    def __str__(self):
        return self.nombre
    
    def cantidad_cursos(self):
        return self.cursos.filter(activo=True).count()