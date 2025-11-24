from django.db import models


class Sector(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Grave(models.Model):
    STATUS_CHOICES = [
        ("available", "Disponible"),
        ("occupied", "Ocupada"),
        ("reserved", "Reservada"),
    ]

    sector = models.ForeignKey(Sector, related_name="graves", on_delete=models.CASCADE)
    code = models.CharField(max_length=50, unique=True)  # Ej: A-01-01
    row = models.CharField(max_length=10, blank=True)
    column = models.CharField(max_length=10, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="available")
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.code


class Deceased(models.Model):
    grave = models.ForeignKey(Grave, related_name="deceased", on_delete=models.PROTECT)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField()
    burial_date = models.DateField()
    document_id = models.CharField(max_length=20, blank=True)  # cédula, etc.

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
