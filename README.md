# 🏛️ SGM – Sistema de Gestión Municipal
### Municipalidad de Guatemala | Prototipo Funcional v1.0

Plataforma web para gestión de trámites, expedientes, pagos y reportes municipales, desarrollada con Python/Flask.

---

## 🚀 Despliegue en Vercel (paso a paso)

### 1. Subir a GitHub
```bash
git init
git add .
git commit -m "feat: SGM prototipo funcional v1.0"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/sgm-municipalidad.git
git push -u origin main
```

### 2. Conectar con Vercel
1. Ir a [vercel.com](https://vercel.com) → **Add New Project**
2. Importar el repositorio de GitHub
3. **Framework Preset:** seleccionar `Other`
4. Hacer clic en **Deploy** — Vercel detecta `vercel.json` automáticamente
5. En ~60 segundos tendrás la URL pública: `https://sgm-municipalidad.vercel.app`

---

## 💻 Ejecución local

```bash
# Clonar / descomprimir el proyecto
cd sgm

# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python app.py
```

Abrir: **http://localhost:5000**

---

## 👤 Usuarios de prueba

| Correo                   | Contraseña | Rol          | Acceso                            |
|--------------------------|------------|--------------|-----------------------------------|
| `ciudadano@gmail.com`    | `1234`     | Ciudadano    | Trámites, solicitudes, pagos      |
| `funcionario@muni.gt`    | `1234`     | Funcionario  | Revisión y aprobación             |
| `admin@muni.gt`          | `1234`     | Administrador| Todo + usuarios + auditoría       |
| `director@muni.gt`       | `1234`     | Director     | Dashboard ejecutivo + reportes    |

---

## 📁 Estructura del Proyecto

```
sgm/
├── app.py                    # Aplicación Flask principal
├── requirements.txt          # Dependencias Python
├── vercel.json               # Configuración de despliegue Vercel
├── .gitignore
├── README.md
├── templates/
│   ├── base.html             # Layout base (sidebar + topbar)
│   ├── login.html            # Inicio de sesión (4 perfiles demo)
│   ├── dashboard_ciudadano.html
│   ├── dashboard_funcionario.html
│   ├── dashboard_ejecutivo.html  # Con gráficas Chart.js
│   ├── tramites.html         # Catálogo de trámites
│   ├── tramite_nuevo.html    # Formulario de solicitud + carga docs
│   ├── tramite_confirmacion.html
│   ├── mis_solicitudes.html  # Lista + filtros + búsqueda
│   ├── expediente_detalle.html   # Timeline + documentos
│   ├── pagos.html            # Pasarela de pago simulada
│   ├── pago_exitoso.html
│   ├── reportes.html         # Reportes + gráficas + exportar
│   ├── presupuesto.html      # Ejecución presupuestal + gráficas
│   ├── inventario.html       # CRUD de bienes municipales
│   ├── usuarios.html         # Gestión de usuarios y roles
│   ├── auditoria.html        # Bitácora del sistema
│   └── perfil.html           # Perfil y configuración
└── static/
    ├── css/main.css          # Design system completo
    └── js/main.js            # Sidebar, toasts, helpers
```

---

## 🖥️ Vistas del Sistema

| Vista | URL | Roles |
|-------|-----|-------|
| Login | `/login` | Todos |
| Dashboard | `/dashboard` | Todos (adaptado por rol) |
| Catálogo Trámites | `/tramites` | Todos |
| Nueva Solicitud | `/tramites/nuevo` | Todos |
| Mis Solicitudes | `/tramites/mis-solicitudes` | Todos |
| Detalle Expediente | `/tramites/expediente/<id>` | Todos |
| Pagos en Línea | `/pagos` | Todos |
| Reportes | `/reportes` | Funcionario, Admin, Director |
| Presupuesto | `/presupuesto` | Funcionario, Admin, Director |
| Inventario | `/inventario` | Funcionario, Admin, Director |
| Usuarios | `/usuarios` | Admin, Director |
| Auditoría | `/auditoria` | Admin, Director |
| Perfil | `/perfil` | Todos |

---

## 🛠️ Tecnologías

- **Backend:** Python 3.11 + Flask 3.0
- **Frontend:** HTML5 + CSS3 (design system propio) + JavaScript vanilla
- **Gráficas:** Chart.js 4.4
- **Deploy:** Vercel (serverless Python)
- **Control de versiones:** Git + GitHub

---

## 📋 Entregable del Proyecto SGM

Este prototipo corresponde al **Entregable 9 (Diseño UI/UX)** y **Entregable 10 (Gestión Ágil)** del proyecto de gestión de software de la Municipalidad de Guatemala, desarrollado siguiendo las buenas prácticas PMBOK y metodología Scrum.
