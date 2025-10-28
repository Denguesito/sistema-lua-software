from django.contrib import admin
from .models import Alumno, RequisitoAlumno

@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('apellido', 'nombre', 'dni', 'edad', 'telefono', 'email', 'pdf_subido', 'requisitos_progreso')
    search_fields = ('apellido', 'nombre', 'dni', 'email', 'telefono')
    list_filter = ('fecha_inscripcion',)
    readonly_fields = ('fecha_inscripcion',)

    def pdf_subido(self, obj):
        return bool(obj.pdf_lua)
    pdf_subido.boolean = True
    pdf_subido.short_description = 'PDF'

    def requisitos_progreso(self, obj):
        entregados, total = obj.requisitos_resumen()
        return f"{entregados}/{total}"

@admin.register(RequisitoAlumno)
class RequisitoAlumnoAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'nombre', 'entregado')
    list_filter = ('entregado',)
    search_fields = ('alumno__apellido', 'alumno__nombre', 'nombre')

