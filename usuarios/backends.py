from django.contrib.auth.backends import ModelBackend
from .models import Usuario
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password
"""
Este módulo define un backend de autenticación personalizado para usuarios.
Permite que los usuarios inicien sesión utilizando su dirección de correo electrónico
en lugar de su nombre de usuario tradicional.
"""

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs): # Método para autenticar a un usuario.
        try: # Intenta obtener un usuario con la dirección de correo electrónico proporcionada.
            user = Usuario.objects.get(email__iexact=username)
        except ObjectDoesNotExist:  # Si no se encuentra un usuario, devuelve None.
            return None         
        else: # Si se encuentra un usuario, verifica la contraseña.
            if check_password(password, user.password)and user.is_active: #Se verifica que el usuario este activo
                return user # Si la contraseña es correcta, devuelve el usuario.
        return None # Si la contraseña es incorrecta, devuelve None.

    def get_user(self, user_id): # Método para obtener un usuario por su ID.
        try: # Intenta obtener un usuario con el ID proporcionado.
            return Usuario.objects.get(pk=user_id) # Si se encuentra un usuario, lo devuelve.
        except Usuario.DoesNotExist:    # Si no se encuentra un usuario, devuelve None.
            return None

class RolPermisosBackend(ModelBackend):
    def has_perm(self, user_obj, perm, obj=None):
        # Permisos directos y de grupos (Django default)
        if super().has_perm(user_obj, perm, obj):
            return True
        # Permisos por rol personalizado
        if hasattr(user_obj, 'rol') and user_obj.rol:
            return user_obj.rol.permisos.filter(
                codename=perm.split('.')[-1],
                content_type__app_label=perm.split('.')[0]
            ).exists()
        return False

    def get_all_permissions(self, user_obj, obj=None):
        perms = set(super().get_all_permissions(user_obj, obj))
        if hasattr(user_obj, 'rol') and user_obj.rol:
            perms.update(
                f"{p.content_type.app_label}.{p.codename}"
                for p in user_obj.rol.permisos.all()
            )
        return perms

    def get_group_permissions(self, user_obj, obj=None):
        perms = set(super().get_group_permissions(user_obj, obj))
        if hasattr(user_obj, 'rol') and user_obj.rol:
            perms.update(
                f"{p.content_type.app_label}.{p.codename}"
                for p in user_obj.rol.permisos.all()
            )
        return perms
