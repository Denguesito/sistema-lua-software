# 🧮 Sistema LUA - Tecnicatura en Desarrollo de Software

**Sistema LUA** (Listado Único de Alumnos) es una aplicación web desarrollada en **Python + Django**, diseñada para que el **bedel o personal administrativo** gestione los **alumnos y sus requisitos de inscripción** de forma simple, ordenada y moderna.

---

## 🎯 Objetivo del sistema

El sistema permite registrar y consultar fácilmente los datos personales de los alumnos, verificar qué documentos de inscripción entregaron, y mantener centralizado el control administrativo de la carrera **Tecnicatura Superior en Desarrollo de Software**.

Principales características:

- Carga de alumnos con datos personales, foto y PDF de su LUA.
- Gestión de **requisitos de inscripción** (entregado / pendiente).
- Edición, eliminación y listado de alumnos.
- Interfaz limpia, responsiva y con colores institucionales.
- Acceso protegido por **login** y cierre de sesión seguro.
- Base de datos **SQLite3** incluida por defecto.
- Compatible con despliegue en **PythonAnywhere** o entornos locales.

---

## ⚙️ Requisitos del sistema

- Python 3.10 o superior  
- Django 5.x  
- Bootstrap 5  
- Navegador actualizado (Chrome, Firefox, Edge, etc.)

---

## 🏗️ Instalación y configuración

1. **Cloná el repositorio o copiá los archivos:**

   ```bash
   git clone https://github.com/tuusuario/sistema-lua.git
   cd sistema-lua
   ```

2. **Creá un entorno virtual (recomendado):**

   ```bash
   python -m venv venv
   ```

3. **Activá el entorno:**

   - En Windows:
     ```bash
     venv\Scripts\activate
     ```
   - En Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Instalá las dependencias del proyecto:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Configurá la base de datos y usuarios:**

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Ejecutá el servidor:**

   ```bash
   python manage.py runserver
   ```

7. Accedé desde tu navegador a:  
   👉 `http://127.0.0.1:8000/`

---

## 📂 Estructura principal del proyecto

```
sistema-lua/
│
├── apps/
│   └── lua/                # Aplicación principal (alumnos, requisitos)
│       ├── models.py       # Modelos (Alumno, Requisitos)
│       ├── views.py        # Lógica de vistas
│       ├── urls.py         # Rutas internas
│       ├── forms.py        # Formularios
│       └── templates/lua/  # Vistas HTML
│
├── static/
│   └── css/styles.css      # Estilos institucionales
│
├── templates/
│   ├── base.html           # Layout principal
│   ├── login.html          # Formulario de acceso
│   └── confirmar_logout.html
│
├── manage.py
├── db.sqlite3
├── requirements.txt
└── README.md
```

---

## 🎨 Créditos y autoría

**Desarrollado por:**  
👨‍💻 *Diego Gómez*  
Estudiante de 2° año - Tecnicatura Superior en Desarrollo de Software  
**Instituto de Educación Superior Machagai (Chaco, Argentina)**

**Año:** 2025  
**Licencia:** Uso educativo y demostrativo

---

## 🚀 Despliegue sugerido

El sistema puede ejecutarse tanto localmente como en **PythonAnywhere**.

Para subirlo:
- Crear el entorno virtual en PythonAnywhere.  
- Subir el código y ejecutar `pip install -r requirements.txt`.  
- Configurar el WSGI y las variables de entorno (DEBUG, ALLOWED_HOSTS).  
- Correr migraciones y crear un superusuario.

---

## 🧰 Dependencias recomendadas

Las principales librerías utilizadas son:

```
Django
Pillow
```

(Otras dependencias se listan automáticamente en `requirements.txt`.)

---

## 🧾 Licencia

Este proyecto está distribuido con fines **educativos** dentro del ámbito de la Tecnicatura Superior en Desarrollo de Software.  
Podés reutilizarlo o adaptarlo libremente con fines de aprendizaje.
