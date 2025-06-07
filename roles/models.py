from django.db import models
from django.contrib.auth.models import Permission
# Create your models here.

class Roles(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=50, unique=True)  # unique= true evita duplicados
    descripcion_rol = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    permisos = models.ManyToManyField(Permission, blank=True, related_name='roles_asociados')

    class Meta:
        db_table = 'roles'
        db_table_comment = 'Esta tabla almacena los roles disponibles en el sistema, como admin, usuario, etc.'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
        

    def __str__(self):
        return self.nombre_rol


