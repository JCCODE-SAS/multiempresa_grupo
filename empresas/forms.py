from django import forms
from .models import Empresa

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre', 'nit', 'correo_corporativo', 'telefono', 'direccion', 'pais']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la Empresa'}),
            'nit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NIT'}),
            'correo_corporativo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico Corporativo'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono Empresarial'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Dirección', 'rows': 3}),
            'pais': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'País'}),
        }