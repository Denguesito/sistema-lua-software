from django import forms
from .models import Alumno
from django.core.exceptions import ValidationError
from django.utils.text import slugify
import json, os
from django.conf import settings

# =============================
# Utilidad para leer requisitos
# =============================
def load_requisitos():
    path = os.path.join(settings.BASE_DIR.parent, 'static', 'lua', 'requisitos.json')
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [{"key": f"req_{slugify(r['nombre'])}", "nombre": r["nombre"]} for r in data]


# =============================
# Formulario de Alumno
# =============================
class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['nombre', 'apellido', 'dni', 'direccion', 'edad', 'telefono', 'email', 'foto', 'pdf_lua']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'pdf_lua': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
        }

    def clean_pdf_lua(self):
        pdf = self.cleaned_data.get('pdf_lua')
        if not pdf:
            raise ValidationError("Debe subir el PDF LUA, es obligatorio.")
        if not pdf.name.lower().endswith('.pdf'):
            raise ValidationError("El archivo debe tener formato PDF.")
        return pdf


# =============================
# Formulario dinámico de requisitos
# =============================
class RequisitosForm(forms.Form):
    def __init__(self, *args, initial_states=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.requisitos = load_requisitos()
        for item in self.requisitos:
            key = item['key']
            label = item['nombre']
            initial = False
            if initial_states and key in initial_states:
                initial = bool(initial_states[key])
            self.fields[key] = forms.BooleanField(
                required=False,
                initial=initial,
                label=label,
                widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
            )
