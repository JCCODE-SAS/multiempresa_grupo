from django import forms
from django.contrib.auth.models import Permission
from .models import Roles
from usuarios.models import Usuario
import re

class RolPermisosForm(forms.ModelForm):
    permisos = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.filter(codename__in=[
            'puede_crear_empresa',
            'puede_editar_empresa',
            'puede_activar_desactivar_empresa',
            'puede_ver_lista_empresas',
            'puede_ver_auditoria',
            'puede_gestionar_usuarios',
            'puede_gestionar_roles',
        ]),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'permiso-personalizado'}),
        required=False,
        label="Permisos del Rol"
    )

    class Meta:
        model = Roles
        fields = ['nombre_rol', 'descripcion_rol', 'permisos']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar los permisos relevantes
        self.fields['permisos'].queryset = Permission.objects.filter(codename__in=[
            'puede_crear_empresa',
            'puede_editar_empresa',
            'puede_activar_desactivar_empresa',
            'puede_ver_lista_empresas',
            'puede_ver_auditoria',
            'puede_gestionar_usuarios',
            'puede_gestionar_roles',
        ])
        def label_perm(obj):
            return obj.name
        self.fields['permisos'].label_from_instance = label_perm

    def clean_permisos(self):
        # Solo permite guardar permisos válidos
        permisos = self.cleaned_data.get('permisos', [])
        permisos_validos = Permission.objects.filter(codename__in=[
            'puede_crear_empresa',
            'puede_editar_empresa',
            'puede_activar_desactivar_empresa',
            'puede_ver_lista_empresas',
            'puede_ver_auditoria',
            'puede_gestionar_usuarios',
            'puede_gestionar_roles',
        ])
        return permisos.intersection(permisos_validos)
