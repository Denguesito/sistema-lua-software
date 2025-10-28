from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

telefono_validator = RegexValidator(
    regex=r'^[0-9+\-\s()]{6,20}$',
    message='Ingrese un teléfono válido (solo dígitos, +, -, espacios y paréntesis).'
)

class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(max_length=200, blank=True)
    edad = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(14), MaxValueValidator(120)],
        help_text="Edad en años (14 a 120)."
    )
    telefono = models.CharField(max_length=30, validators=[telefono_validator], blank=True)
    email = models.EmailField(blank=True)

    # Archivos
    foto = models.ImageField(upload_to='fotos/', blank=True, null=True)   # opcional
    pdf_lua = models.FileField(upload_to='pdfs/')                         # obligatorio

    fecha_inscripcion = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['apellido', 'nombre']
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def requisitos_resumen(self):
        """Devuelve (entregados, total) para usar en listados."""
        total = self.requisitos.count()
        entregados = self.requisitos.filter(entregado=True).count()
        return entregados, total


class RequisitoAlumno(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='requisitos')
    nombre = models.CharField(max_length=120)  # viene del JSON estático
    entregado = models.BooleanField(default=False)

    class Meta:
        ordering = ['nombre']
        unique_together = ('alumno', 'nombre')
        verbose_name = 'Requisito del alumno'
        verbose_name_plural = 'Requisitos del alumno'

    def __str__(self):
        estado = 'Entregado' if self.entregado else 'Pendiente'
        return f"{self.nombre} - {estado} ({self.alumno})"
