# Multiempresa Grupo

Sistema Django multiempresa para administración de empresas y usuarios, con enfoque en modularidad, responsividad y experiencia de usuario moderna.

## Características principales
- Gestión de empresas: creación, edición, activación/desactivación, auditoría.
- Administración de usuarios: roles, activación/desactivación, edición, archivado.
- Panel administrativo centralizado.
- Formularios y tablas responsivos y accesibles.
- Confirmaciones de acciones críticas con SweetAlert2.
- Modularización de navbar, scripts y estilos.
- Integración de Bootstrap 5 y Bootstrap Icons.

## Estructura del proyecto
- `usuarios/`: gestión de usuarios, roles y autenticación.
- `empresas/`: gestión de empresas.
- `admin_empresas/`: administración avanzada de empresas.
- `roles/`, `seguridad/`: módulos de roles y seguridad.
- `static/`: archivos CSS y JS globales y específicos por vista.
- `templates/`: plantillas HTML organizadas por app.

## Instalación rápida
1. Clona el repositorio:
   ```bash
   git clone <URL-del-repo>
   cd multiempresa_grupo
   ```
2. Crea y activa un entorno virtual:
   ```bash
   python -m venv envs
   envs\Scripts\activate  # Windows
   # source envs/bin/activate  # Linux/Mac
   ```
3. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Aplica migraciones:
   ```bash
   python manage.py migrate
   ```
5. Crea un superusuario:
   ```bash
   python manage.py createsuperuser
   ```
6. Ejecuta el servidor:
   ```bash
   python manage.py runserver
   ```

## Uso
- Accede a `/usuarios/login/` para iniciar sesión.
- Panel administrativo: `/usuarios/panel_administrativo/`
- Administración de empresas: `/admin_empresas/lista_empresas/`
- Administración de usuarios: `/usuarios/administracion_usuarios/`

## Notas técnicas
- Los archivos estáticos están organizados en `static/css/` y `static/js/`.
- Navbar, scripts y estilos son modulares y reutilizables.
- Confirmaciones de acciones críticas usan SweetAlert2.
- El proyecto es fácilmente escalable para nuevas vistas y módulos.

## Créditos y documentación
- [Guía de estructura y cambios](https://drive.google.com/file/d/1XEerwGZbPgH2vrooAdKAbaqHor5KGaQE/view?usp=sharing)
- [Guía de instalación y clonado](https://drive.google.com/file/d/1E1wH8TaEaXGPDtqMQCjPf2H3dTRfYB9C/view?usp=sharing)

---
Desarrollado por el equipo Multiempresa Grupo.
