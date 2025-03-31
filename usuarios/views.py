from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from roles.models import Roles #se agrega la importacion de Roles
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required #se agrega la importacion de permission_required
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model
import random  # Importar el módulo random
import string #Importa el modulo string
import uuid  # Importar el módulo uuid para generar tokens únicos
from django.core.mail import send_mail  # Importa la función para enviar correos
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
from .models import Usuario,IntentosFallidos, Sesiones, CambioContrasena
# este metodo se encarga de registrar un usuario
def register_view(request):
    if request.method == 'POST': #se agrego el metodo post
        # Se obtienen los datos del formulario
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        password2 = request.POST.get('password2').strip()
        email = request.POST.get('email').strip()
        email2 = request.POST.get('email2').strip()
        # Se validan los datos
        if not username or not password or not password2 or not email or not email2:
            return JsonResponse({'error': 'Faltan campos obligatorios'}, status=400, json_dumps_params={'ensure_ascii': False})
        # Se validan las contraseñas y correos electrónicos Coinciden
        if password != password2:
            return JsonResponse({'error': 'Las contraseñas no coinciden'}, status=400, json_dumps_params={'ensure_ascii': False})
        
        if email != email2:
            return JsonResponse({'error': 'Los correos electrónicos no coinciden'}, status=400, json_dumps_params={'ensure_ascii': False})
        # Se verifica si el usuario o correo electrónico ya están en uso
        if Usuario.objects.filter(email=email).exists():
            return JsonResponse({'error': 'El correo electrónico ya está en uso'}, status=400, json_dumps_params={'ensure_ascii': False})

        if Usuario.objects.filter(username=username).exists():
            sugerencia = generar_sugerencia_username(username)
            return JsonResponse({'error': 'El nombre de usuario ya está en uso', 'sugerencia': sugerencia}, status=400, json_dumps_params={'ensure_ascii': False})
        
        # Se hashea la contraseña para almacenarla de forma segura y que es hashea, es  decir, se convierte en una cadena de caracteres aleatoria para complicar su descifrado    
        hashed_password = make_password(password)
        # Se crea el usuario
        user = Usuario.objects.create(username=username, password=hashed_password, email=email, is_active=False)
        user.save() # Se guarda el usuario en la base de datos
        return JsonResponse({'message': 'Usuario registrado exitosamente'}, status=201, json_dumps_params={'ensure_ascii': False})  # Se responde con un mensaje de éxito

    elif request.method == 'GET': #se agrego el metodo get para mostrar la pagina de registro
        return render(request, 'usuarios/registro.html')    # RENDERIZA LA NUEVA PAGINA DE REGISTRO
    else: #se agrego el metodo else para mostrar un mensaje de error si el metodo no es permitido
        return JsonResponse({'error': 'Método no permitido'}, status=405, json_dumps_params={'ensure_ascii': False})

# este metodo se encarga de generar una sugerencia de username
def generar_sugerencia_username(username):
    while True: # Ciclo para generar sugerencias hasta encontrar un username disponible
        numero_aleatorio = ''.join(random.choices(string.digits, k=4)) # produce una cadena de 4 dígitos aleatorios
        nuevo_username = f"{username}_{numero_aleatorio}" # Se crea un nuevo username_con el número aleatorio ultilizando f string  para concatenar
        if not Usuario.objects.filter(username=nuevo_username).exists(): # Si el username no está en uso, se retorna
            return nuevo_username # Se retorna el nuevo username

# este metodo se encarga de iniciar sesion        
def login_view(request):
    # Se valida el método de la solicitud y se obtienen los datos del formulario en formato JSON
    if request.method == 'POST':
        data = json.loads(request.body)
        email_or_username = data.get('username')
        password = data.get('password')

        if not email_or_username or not password: # Se verifica que los campos no estén vacíos
            return JsonResponse({'error': 'Faltan campos obligatorios'}, status=400, json_dumps_params={'ensure_ascii': False})
        # Se autentica al usuario
        user = authenticate(request, username=email_or_username, password=password) # Se autentica al usuario con el username o email y la contraseña

        if user is not None: # Si el usuario es autenticado correctamente
            login(request, user) # se inicia sesion correctamente
            # Se crea un token de sesión para el usuario
            token_sesion = str(uuid.uuid4())
            Sesiones.objects.create(
                id_usuario=user,
                token_sesion=token_sesion, # Se crea un token de sesión único
                fecha_inicio=timezone.now(),    # Se obtiene la fecha y hora actual
                ip_usuario=request.META.get('REMOTE_ADDR'), # Se obtiene la dirección IP del cliente
                agente_usuario=request.META.get('HTTP_USER_AGENT')  # Se obtiene el agente de usuario del cliente
            )
            return JsonResponse({'message': 'Login exitoso'}, status=200, json_dumps_params={'ensure_ascii': False})
        else: # Si las credenciales son inválidas
            try:    # Se intenta obtener el usuario con el email o username
                usuario = Usuario.objects.get(email=email_or_username) # Se obtiene el usuario con el email o username
                if not usuario.is_active: # Se verifica si el usuario está activo
                    return JsonResponse({'error': 'Usuario inactivo. Por favor, espera a que el administrador active tu cuenta.'}, status=400, json_dumps_params={'ensure_ascii': False})
                IntentosFallidos.objects.create( # Se registra el intento fallido en la base de datos
                    id_usuario=usuario,
                    ip_usuario=request.META.get('REMOTE_ADDR'),
                    fecha_intento=timezone.now()
                )
            except Usuario.DoesNotExist: # Si el usuario no existe, se pasa
                pass
            return JsonResponse({'error': 'Credenciales inválidas'}, status=400, json_dumps_params={'ensure_ascii': False})
    
    elif request.method == 'GET':
        return render(request, 'usuarios/login.html') # renderiza a la pagina de login
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405, json_dumps_params={'ensure_ascii': False})
from django.shortcuts import redirect

def home_view(request):
    return redirect('usuarios:login')  # Redirige a la página de inicio de sesión
    
# este metodo se encarga de cerrar sesion
def logout_view(request):
    sesion = Sesiones.objects.filter(id_usuario=request.user, fecha_fin__isnull=True).last()
    if sesion:
        sesion.fecha_fin = timezone.now()
        sesion.save()
    logout(request)
    return redirect('usuarios:login')  # Redirige a la página de inicio de sesión


# este metodo se encarga de mostrar la pagina de administracion de usuarios
@login_required  # El decorador @login_required es una herramienta proporcionada por Django para restringir el acceso a una vista solo a usuarios que han iniciado sesión.
def admin_usuarios_view(request):
    if request.method == 'GET':
        return render(request, 'usuarios/admin_usuarios.html')  # RENDERIZA LA PAGINA DE ADMINISTRACION DE USUARIOS aclaro no es la de django admin
    elif request.method == 'POST':  # se agrego el metodo post
        # Se obtiene la sesión activa del usuario
        sesion = Sesiones.objects.filter(id_usuario=request.user, fecha_fin__isnull=True).last()
        if sesion:  # Si la sesión existe, se cierra
            sesion.fecha_fin = timezone.now()
            sesion.save()
        logout(request)
        return redirect('usuarios:login')  # Redirige a la página de inicio de sesión
    else:
        return redirect('usuarios:login')  # Redirige también si el método no es POS
#  Vista para cambiar la contraseña de un usuario logueado.
@login_required #El decorador @login_required es una herramienta proporcionada por Django para restringir el acceso a una vista solo a usuarios que han iniciado sesión.
def cambio_contrasena_view(request):
    # Se valida el método de la solicitud
    if request.method == 'POST':
        # Se obtiene la nueva contraseña del formulario
        nueva_contrasena = request.POST.get('nueva_contrasena')
        request.user.set_password(nueva_contrasena)
        request.user.save() # Se guarda el usuario con la nueva contraseña
        CambioContrasena.objects.create(  # Se registra el cambio de contraseña en la base de datos  
            id_usuario=request.user,
            fecha_cambio=timezone.now(),
            ip_usuario=request.META.get('REMOTE_ADDR')
        )
        return JsonResponse({'success': True})  # Se responde con un mensaje de éxito
    
    return render(request, 'usuarios/cambio_contrasena.html')   

# este metodo se encarga de mostrar la pagina de registro exitoso
def registro_exitoso(request):
    return render(request, 'usuarios/registro_exitoso.html')


# este metodo se encarga de generar un token de recuperacion  
def generar_token_recuperacion():
    """Genera un token único para la recuperación de contraseña."""
    return str(uuid.uuid4())


# este metodo se encarga de recuperar la contraseña
def recuperar_contrasena_view(request):
    """Vista para manejar la solicitud de recuperación de contraseña."""
    if request.method == 'POST':
        try:
            # Se obtiene el correo electrónico del cuerpo de la solicitud en formato JSON
            data = json.loads(request.body)
            email = data.get('email')
            confirmEmail = data.get('confirmEmail')
            if email != confirmEmail: # Se verifica que los correos electrónicos coincidan
                return JsonResponse({'error': 'Los correos electrónicos no coinciden'}, status=400)
            usuario = get_object_or_404(Usuario, email=email) # Se obtiene el usuario con el correo electrónico
            token = generar_token_recuperacion() # Se genera un token de recuperación
            # Guarda el token en el modelo de usuario (o en un modelo separado para tokens)
            usuario.token_recuperacion = token # Se guarda el token en el usuario y en la variable token
            usuario.save()
            enviar_correo_recuperacion(usuario, token) # Se envía el correo electrónico con el enlace de recuperación
            return JsonResponse({'message': 'Correo de recuperación enviado'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Datos inválidos'}, status=400)
    elif request.method == 'GET':
        return render(request, 'usuarios/recuperar_contrasena.html')    
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

def enviar_correo_recuperacion(usuario, token):
    """Envía un correo electrónico con el enlace de recuperación de contraseña."""
    # Crea el enlace de recuperación
    enlace_recuperacion = f"http://127.0.0.1:8000/usuarios/restablecer_contrasena/{usuario.id}/{token}/"
    
    # Renderiza la plantilla del correo electrónico
    html_content = render_to_string('usuarios/email_recuperacion.html', {'enlace': enlace_recuperacion, 'usuario': usuario}) # Renderiza la plantilla del correo electrónico y pasa el enlace y el usuario
    text_content = 'This is an important message.' # Crea un mensaje de texto plano

    # Crea el correo electrónico
    msg = EmailMultiAlternatives( # Crea un objeto EmailMultiAlternatives que permite enviar correos con contenido HTMl
        'Recuperación de Contraseña', 
        text_content,
        'tu-correo@tu-dominio.com', 
        [usuario.email]
    )
    msg.attach_alternative(html_content, "text/html") # Adjunta el contenido HTML al correo electrónico
    msg.send() # Envía el correo electrónico
    
# este metodo se encarga de restablecer la contraseña al usuario que olvido su contraseña       
def restablecer_contrasena_view(request, usuario_id, token):
    """Vista para restablecer la contraseña y registrar el cambio en CambioContrasena."""
    usuario = get_object_or_404(Usuario, id=usuario_id, token_recuperacion=token)
    if request.method == 'POST':
        nueva_contrasena = request.POST.get('nueva_contrasena')
        usuario.set_password(nueva_contrasena)
        usuario.token_recuperacion = None  # Invalida el token después de usarlo
        usuario.save()

        # Registra el cambio de contraseña usando la lógica de tu función
        CambioContrasena.objects.create(
            id_usuario=usuario,
            fecha_cambio=timezone.now(),
            ip_usuario=request.META.get('REMOTE_ADDR', '0.0.0.0') #Agregado valor por defecto
        )

        return HttpResponseRedirect(reverse('login'))  # Redirige al login
    return render(request, 'usuarios/restablecer_contrasena.html', {'usuario': usuario})

@login_required
@permission_required('usuarios.view_usuario', raise_exception=True)
def gestionar_usuarios_view(request):
    """
    Vista para administrar usuarios. Permite listar, filtrar, activar/desactivar,
    cambiar roles y archivar usuarios.
    """
    usuarios = Usuario.objects.all().order_by('username')
    roles = Roles.objects.all()

    # Filtros
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
        user_id = request.POST.get('user_id')
        usuario = get_object_or_404(Usuario, id=user_id)

        if action == 'activar':
            usuario.is_active = True
            usuario.save()
            print(f"Usuario {usuario.id} activado.")

        elif action == 'cambiar_rol':
            nuevo_rol_id = request.POST.get('nuevo_rol')
            nuevo_rol = get_object_or_404(Roles, id_rol=nuevo_rol_id)
            usuario.rol = nuevo_rol
            usuario.save()
        elif action == 'desactivar':
            usuario.is_active = False
            usuario.save()
        elif action == 'archivar':
            usuario.is_active = False
            usuario.save()

        return redirect('usuarios:gestionar_usuarios')

    context = {
        'usuarios': usuarios,
        'roles': roles,
        'filtro_username': filtro_username,
        'filtro_email': filtro_email,
        'filtro_rol': filtro_rol,
        'filtro_activo': filtro_activo,
    }
    return render(request, 'usuarios/gestionar_usuarios.html', context)
@login_required
@permission_required('usuarios.change_usuario', raise_exception=True)
def editar_usuario_view(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        # Procesar el formulario de edición
        usuario.username = request.POST.get('username')
        usuario.email = request.POST.get('email')
        # ... otros campos ...
        usuario.save()
        return redirect('usuarios:gestionar_usuarios')  # Redirigir a la lista de usuarios #se cambio el nombre de la url
    else:
        # Mostrar el formulario de edición
        context = {'usuario': usuario}
        return render(request, 'usuarios/editar_usuario.html', context)