from django.urls import path
from . import views

app_name = 'lua'

urlpatterns = [
    # Página principal (menú o dashboard)
    path('', views.MenuPrincipalView.as_view(), name='menu'),

    # CRUD de alumnos
    path('alumnos/', views.AlumnoListView.as_view(), name='lista_alumnos'),
    path('alumnos/nuevo/', views.AlumnoCreateView.as_view(), name='crear_alumno'),
    path('alumnos/<int:pk>/', views.AlumnoDetailView.as_view(), name='detalle_alumno'),
    path('alumnos/<int:pk>/editar/', views.AlumnoUpdateView.as_view(), name='editar_alumno'),
    path('alumnos/<int:pk>/eliminar/', views.AlumnoDeleteView.as_view(), name='eliminar_alumno'),
]
