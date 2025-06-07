from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from roles.models import Roles

# Lista de permisos personalizados válidos
PERMISOS_VALIDOS = [
    'puede_crear_empresa',
    'puede_editar_empresa',
    'puede_activar_desactivar_empresa',
    'puede_ver_lista_empresas',
    'puede_ver_auditoria',
    'puede_gestionar_usuarios',
]

class Command(BaseCommand):
    help = 'Limpia los roles antiguos eliminando permisos no personalizados válidos.'

    def handle(self, *args, **options):
        permisos_validos = Permission.objects.filter(codename__in=PERMISOS_VALIDOS)
        roles = Roles.objects.all()
        for rol in roles:
            permisos_rol = rol.permisos.all()
            permisos_a_remover = permisos_rol.exclude(codename__in=PERMISOS_VALIDOS)
            if permisos_a_remover.exists():
                rol.permisos.remove(*permisos_a_remover)
                self.stdout.write(self.style.WARNING(f"Permisos obsoletos eliminados del rol: {rol.nombre_rol}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Rol limpio: {rol.nombre_rol}"))
        self.stdout.write(self.style.SUCCESS('Limpieza de roles completada.'))
