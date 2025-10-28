from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Alumno, RequisitoAlumno
from .forms import AlumnoForm, RequisitosForm
from .forms import load_requisitos


# =============================
# MENÚ PRINCIPAL
# =============================
class MenuPrincipalView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"


# =============================
# LISTADO DE ALUMNOS (CARDS)
# =============================
class AlumnoListView(LoginRequiredMixin, ListView):
    model = Alumno
    template_name = "lua/lista_alumnos.html"
    context_object_name = "alumnos"
    paginate_by = 8  # si querés paginar las cards (opcional)

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Alumno.objects.filter(
                nombre__icontains=query
            ) | Alumno.objects.filter(apellido__icontains=query)
        return Alumno.objects.all()


# =============================
# CREAR ALUMNO
# =============================
class AlumnoCreateView(LoginRequiredMixin, CreateView):
    model = Alumno
    form_class = AlumnoForm
    template_name = "lua/crear_alumno.html"
    success_url = reverse_lazy("lua:lista_alumnos")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["requisitos_form"] = RequisitosForm(self.request.POST or None)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        requisitos_form = context["requisitos_form"]

        if requisitos_form.is_valid():
            alumno = form.save()

            # Cargar los requisitos desde el JSON y guardar los estados
            requisitos = load_requisitos()
            for item in requisitos:
                key = item["key"]
                nombre = item["nombre"]
                entregado = requisitos_form.cleaned_data.get(key, False)
                RequisitoAlumno.objects.create(
                    alumno=alumno, nombre=nombre, entregado=entregado
                )

            messages.success(self.request, f"Alumno {alumno.nombre_completo} creado correctamente.")
            return redirect(self.success_url)

        messages.error(self.request, "Revisá los datos del formulario.")
        return self.form_invalid(form)


# =============================
# DETALLE DE ALUMNO
# =============================
class AlumnoDetailView(LoginRequiredMixin, DetailView):
    model = Alumno
    template_name = "lua/detalle_alumno.html"
    context_object_name = "alumno"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        alumno = self.get_object()
        entregados, total = alumno.requisitos_resumen()
        context["progreso"] = f"{entregados}/{total}"
        context["requisitos"] = alumno.requisitos.all()
        return context


# =============================
# EDITAR ALUMNO
# =============================
class AlumnoUpdateView(LoginRequiredMixin, UpdateView):
    model = Alumno
    form_class = AlumnoForm
    template_name = "lua/editar_alumno.html"
    success_url = reverse_lazy("lua:lista_alumnos")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        alumno = self.get_object()

        # Estados actuales de requisitos
        requisitos = load_requisitos()
        current_states = {}
        existentes = {r.nombre: r for r in alumno.requisitos.all()}
        for item in requisitos:
            nombre = item["nombre"]
            req = existentes.get(nombre)
            current_states[item["key"]] = req.entregado if req else False

        context["requisitos_form"] = RequisitosForm(
            self.request.POST or None, initial_states=current_states
        )
        return context

    def form_valid(self, form):
        alumno = form.save(commit=False)
        context = self.get_context_data()
        requisitos_form = context["requisitos_form"]

        if requisitos_form.is_valid():
            alumno.save()
            requisitos = load_requisitos()
            for item in requisitos:
                key = item["key"]
                nombre = item["nombre"]
                entregado = requisitos_form.cleaned_data.get(key, False)
                req, _ = RequisitoAlumno.objects.get_or_create(
                    alumno=alumno, nombre=nombre
                )
                req.entregado = entregado
                req.save()

            messages.success(self.request, f"Datos de {alumno.nombre_completo} actualizados correctamente.")
            return redirect(self.success_url)

        messages.error(self.request, "Revisá los datos del formulario.")
        return self.form_invalid(form)


# =============================
# ELIMINAR ALUMNO
# =============================
class AlumnoDeleteView(LoginRequiredMixin, DeleteView):
    model = Alumno
    template_name = "lua/eliminar_alumno.html"
    success_url = reverse_lazy("lua:lista_alumnos")

    def delete(self, request, *args, **kwargs):
        alumno = self.get_object()
        messages.warning(request, f"Alumno {alumno.nombre_completo} eliminado.")
        return super().delete(request, *args, **kwargs)


@login_required
def confirmar_logout(request):
    """
    GET  -> muestra pantalla de confirmación
    POST -> cierra sesión y redirige al menú principal
    """
    if request.method == "POST":
        logout(request)
        return redirect('lua:menu')   # <- tu página menú / index
    return render(request, 'confirmar_logout.html')
