# usuarios/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from roles.models import Roles
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model
import random
import string
import uuid
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q

"""
Este módulo define las vistas (controladores) de la aplicación 'usuarios'.
Contiene las funciones que gestionan las solicitudes HTTP relacionadas con:
- Registro de usuarios.
- Inicio de sesión y cierre de sesión.
- Administración de usuarios (panel).
- Cambio de contraseña.
- Recuperación de contraseña (envío de correo y restablecimiento).
"""
from .models import Usuario, IntentosFallidos, Sesiones, CambioContrasena, UsuarioArchivado

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        password2 = request.POST.get('password2').strip()
        email = request.POST.get('email').strip()
        email2 = request.POST.get('email2').strip()

        if not username or not password or not password2 or not email or not email2:
            return JsonResponse({'error': 'Faltan campos obligatorios'}, status=400, json_dumps_params={'ensure_ascii': False})

        if password != password2:
            return JsonResponse({'error': 'Las contraseñas no coinciden'}, status=400, json_dumps_params={'ensure_ascii': False})

        if email != email2:
            return JsonResponse({'error': 'Los correos electrónicos no coinciden'}, status=400, json_dumps_params={'ensure_ascii': False})

        if Usuario.objects.filter(email=email).exists():
            return JsonResponse({'error': 'El correo electrónico ya está en uso'}, status=400, json_dumps_params={'ensure_ascii': False})

        if Usuario.objects.filter(username=username).exists():
            sugerencia = generar_sugerencia_username(username)
            return JsonResponse({'error': 'El nombre de usuario ya está en uso', 'sugerencia': sugerencia}, status=400, json_dumps_params={'ensure_ascii': False})

        hashed_password = make_password(password)
        user = Usuario.objects.create(username=username, password=hashed_password, email=email, is_active=False)
        user.save()
        return JsonResponse({'message': 'Usuario registrado exitosamente'}, status=201, json_dumps_params={'ensure_ascii': False})

    elif request.method == 'GET':
        return render(request, 'usuarios/registro.html')
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405, json_dumps_params={'ensure_ascii': False})

def generar_sugerencia_username(username):
    while True:
        numero_aleatorio = ''.join(random.choices(string.digits, k=4))
        nuevo_username = f"{username}_{numero_aleatorio}"
        if not Usuario.objects.filter(username=nuevo_username).exists():
            return nuevo_username

def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email_or_username = data.get('username')
        password = data.get('password')

        if not email_or_username or not password:
            return JsonResponse({'error': 'Faltan campos obligatorios'}, status=400, json_dumps_params={'ensure_ascii': False})

        user = authenticate(request, username=email_or_username, password=password)

        if user is not None:
            login(request, user)
            token_sesion = str(uuid.uuid4())
            Sesiones.objects.create(
                id_usuario=user,
                token_sesion=token_sesion,
                fecha_inicio= timezone.now(),
                ip_usuario=request.META.get('REMOTE_ADDR'),
                agente_usuario=request.META.get('HTTP_USER_AGENT')
            )
            return JsonResponse({'message': 'Login exitoso'}, status=200, json_dumps_params={'ensure_ascii': False})
        else:
            try:
                usuario = Usuario.objects.get(email=email_or_username)
                if not usuario.is_active:
                    return JsonResponse({'error': 'Usuario inactivo. Por favor, espera a que el administrador active tu cuenta.'}, status=400, json_dumps_params={'ensure_ascii': False})
                IntentosFallidos.objects.create(
                    id_usuario=usuario,
                    ip_usuario=request.META.get('REMOTE_ADDR'),
                    fecha_intento=timezone.now()
                )
            except Usuario.DoesNotExist:
                pass
            return JsonResponse({'error': 'Credenciales inválidas'}, status=400, json_dumps_params={'ensure_ascii': False})

    elif request.method == 'GET':
        return render(request, 'usuarios/login.html')
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405, json_dumps_params={'ensure_ascii': False})

def home_view(request):
    return redirect('usuarios:login')

def logout_view(request):
    sesion = Sesiones.objects.filter(id_usuario=request.user, fecha_fin__isnull=True).last()
    if sesion:
        sesion.fecha_fin = timezone.now()
        sesion.save()
    logout(request)
    return redirect('usuarios:login')

@login_required
def panel_administrativo_view(request):
    if request.method == 'GET':
        return render(request, 'usuarios/panel_administrativo.html')
    elif request.method == 'POST':
        sesion = Sesiones.objects.filter(id_usuario=request.user, fecha_fin__isnull=True).last()
        if sesion:
            sesion.fecha_fin = timezone.now()
            sesion.save()
        logout(request)
        return redirect('usuarios:login')
    else:
        return redirect('usuarios:login')

@login_required
def cambio_contrasena_view(request):
    if request.method == 'POST':
        nueva_contrasena = request.POST.get('nueva_contrasena')
        request.user.set_password(nueva_contrasena)
        request.user.save()
        CambioContrasena.objects.create(
            id_usuario=request.user,
            fecha_cambio=timezone.now(),
            ip_usuario=request.META.get('REMOTE_ADDR')
        )
        return JsonResponse({'success': True})

    return render(request, 'usuarios/cambio_contrasena.html')

def registro_exitoso(request):
    return render(request, 'usuarios/registro_exitoso.html')

def generar_token_recuperacion():
    """Genera un token único para la recuperación de contraseña."""
    return str(uuid.uuid4())

def recuperar_contrasena_view(request):
    """Vista para manejar la solicitud de recuperación de contraseña."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            confirmEmail = data.get('confirmEmail')
            if email != confirmEmail:
                return JsonResponse({'error': 'Los correos electrónicos no coinciden'}, status=400)
            usuario = get_object_or_404(Usuario, email=email)
            token = generar_token_recuperacion()
            usuario.token_recuperacion = token
            usuario.save()
            enviar_correo_recuperacion(usuario, token)
            return JsonResponse({'message': 'Correo de recuperación enviado'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Datos inválidos'}, status=400)
    elif request.method == 'GET':
        return render(request, 'usuarios/recuperar_contrasena.html')
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

def enviar_correo_recuperacion(usuario, token):
    """Envía un correo electrónico con el enlace de recuperación de contraseña."""
    enlace_recuperacion = f"http://127.0.0.1:8000/usuarios/restablecer_contrasena/{usuario.id}/{token}/"

    html_content = render_to_string('usuarios/email_recuperacion.html', {'enlace': enlace_recuperacion, 'usuario': usuario})
    text_content = 'This is an important message.'

    msg = EmailMultiAlternatives(
        'Recuperación de Contraseña',
        text_content,
        'tu-correo@tu-dominio.com',
        [usuario.email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def restablecer_contrasena_view(request, usuario_id, token):
    """Vista para restablecer la contraseña y registrar el cambio en CambioContrasena."""
    usuario = get_object_or_404(Usuario, id=usuario_id, token_recuperacion=token)
    if request.method == 'POST':
        nueva_contrasena = request.POST.get('nueva_contrasena')
        usuario.set_password(nueva_contrasena)
        usuario.token_recuperacion = None
        usuario.save()

        CambioContrasena.objects.create(
            id_usuario=usuario,
            fecha_cambio=timezone.now(),
            ip_usuario=request.META.get('REMOTE_ADDR', '0.0.0.0')
        )

        return HttpResponseRedirect(reverse('login'))
    return render(request, 'usuarios/restablecer_contrasena.html', {'usuario': usuario})

@login_required
@permission_required('usuarios.view_usuario', raise_exception=True)
def administracion_usuarios_view(request):
    print("--- DEBUG: administracion_usuarios_view iniciada ---")
    """
    Vista para administrar usuarios. Permite listar, filtrar, activar/desactivar,
    cambiar roles y archivar usuarios.
    """
    ids_archivados = UsuarioArchivado.objects.values_list('usuario_archivado_id', flat=True)
    usuarios = Usuario.objects.exclude(id__in=ids_archivados).order_by('username')
    roles = Roles.objects.all()

    filtro_username = request.GET.get('username', '')
    filtro_email = request.GET.get('email', '')
    filtro_rol = request.GET.get('rol', '')
    filtro_activo = request.GET.get('activo', '')

    if filtro_username:
        usuarios = usuarios.filter(username__icontains=filtro_username)
    if filtro_email:
        usuarios = usuarios.filter(email__icontains=filtro_email)
    if filtro_rol:
        usuarios = usuarios.filter(rol_id=filtro_rol)
    if filtro_activo:
        usuarios = usuarios.filter(is_active=(filtro_activo == 'true'))

    if request.method == 'POST':
        print(request.POST)  # Depuración
        action = request.POST.get('action')
        print(f"--- DEBUG: Valor de action: '{action}', Tipo de action: {type(action)} ---") # <<< AÑADE ESTA LÍNEA
        user_id = request.POST.get('user_id')
        usuario = get_object_or_404(Usuario, id=user_id)
        print("--- DEBUG: Justo antes de la cadena if/elif de acciones ---")
        if action == 'activar':
            print("--- DEBUG: Entrando en el bloque if para acción: activar ---") # Debug
            if request.user.has_perm('usuarios.can_change_usuario_status'):
                print("Usuario logueado tiene permiso para cambiar estado (activar).") # Debug
                usuario.is_active = True
                print("Intentando guardar usuario (activar)...") # Debug
                usuario.save()
                print(f"Usuario {usuario.id} activado.") # Debug
            else:
                print("Usuario logueado NO tiene permiso para cambiar estado (activar).") # Debug
                pass

        elif action == 'cambiar_rol':
             print(f"--- DEBUG: Entrando en el bloque elif para acción: {action} ---") # Debug: Added this print
             print("Acción: cambiar_rol") # Debug: Uncommented
             if request.user.has_perm('usuarios.can_change_usuario_rol'):
                print("Usuario logueado tiene permiso para cambiar rol.") # Debug: Uncommented
                nuevo_rol_id = request.POST.get('nuevo_rol')
                print(f"Nuevo Rol ID: {nuevo_rol_id}") # Debug: Uncommented
                nuevo_rol = get_object_or_404(Roles, id_rol=nuevo_rol_id)
                print(f"Nuevo Rol encontrado: {nuevo_rol.nombre_rol}") # Debug: Uncommented
                usuario.rol = nuevo_rol
                print(f"Usuario {usuario.username} rol AHORA es: {usuario.rol.nombre_rol}") # Debug: Uncommented
                print("--- Justo antes de usuario.save() para cambiar_rol ---") # Debug: Uncommented
                usuario.save() # <-- Uncommented this crucial line
                print("--- Justo DESPUÉS de usuario.save() para cambiar_rol ---") # Debug: Uncommented

             else:
                print("Usuario logueado NO tiene permiso para cambiar rol.") # Debug: Uncommented
                pass

        elif action == 'desactivar':
            print("--- DEBUG: Entrando en el bloque elif para acción: desactivar ---") # Debug
            if request.user.has_perm('usuarios.can_change_usuario_status'):
                print("Usuario logueado tiene permiso para cambiar estado (desactivar).") # Debug
                usuario.is_active = False
                print("Intentando guardar usuario (desactivar)...") # Debug
                usuario.save()
                print(f"Usuario {usuario.id} desactivado.") # Debug
            else:
                print("Usuario logueado NO tiene permiso para cambiar estado (desactivar).") # Debug
                pass

        elif action == 'archivar':
            print("--- DEBUG: Entrando en el bloque elif para acción: archivar ---") # Debug
            if request.user.has_perm('usuarios.can_archive_usuario'): # Verifica si tienes este permiso
                print("Usuario logueado tiene permiso para archivar.") # Debug
                motivo_archivo = request.POST.get('motivo_archivo', '')
                print(f"Motivo archivo: {motivo_archivo}") # Debug
                if not UsuarioArchivado.objects.filter(usuario_archivado=usuario).exists():
                    print("Usuario no estaba previamente archivado. Creando registro de archivo...") # Debug
                    UsuarioArchivado.objects.create(
                        usuario_archivado=usuario,
                        archivado_por=request.user,
                        motivo=motivo_archivo
                    )
                    print("Registro de archivo creado. Desactivando usuario...") # Debug
                    usuario.is_active = False # Se desactiva al archivar
                    print("Intentando guardar usuario (archivar/desactivar)...") # Debug
                    usuario.save() # <-- Uncommented this crucial line
                    print(f"Usuario {usuario.id} archivado y desactivado.") # Debug
                else:
                    print("Usuario ya estaba archivado.") # Debug
                    pass
            else:
                print("Usuario logueado NO tiene permiso para archivar.") # Debug
                pass

        return redirect('usuarios:administracion_usuarios')

    context = {
        'usuarios': usuarios,
        'roles': roles,
        'filtro_username': filtro_username,
        'filtro_email': filtro_email,
        'filtro_rol': filtro_rol,
        'filtro_activo': filtro_activo,
    }
    return render(request, 'usuarios/administracion_usuarios.html', context)

@login_required
@permission_required('usuarios.change_usuario', raise_exception=True)
def editar_usuario_view(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        usuario.username = request.POST.get('username')
        usuario.email = request.POST.get('email')
        # ... otros campos ...
        usuario.save()
        return redirect('usuarios:administracion_usuarios')
    else:
        context = {'usuario': usuario}
        return render(request, 'usuarios/editar_usuario.html', context)