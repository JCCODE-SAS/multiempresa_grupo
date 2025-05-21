from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EmpresaForm
from .models import Empresa
from django.db import IntegrityError

def crear_empresa(request):
    empresa_creada = False  # Variable para controlar si se muestra el modal
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            telefono = form.cleaned_data.get('telefono')
            direccion = form.cleaned_data.get('direccion')

            hay_duplicados = False

            # Validaciones personalizadas de duplicados
            if email and Empresa.objects.filter(email__iexact=email).exists():
                form.add_error('email', 'Este correo electrónico ya está registrado.')
                hay_duplicados = True
            if telefono and Empresa.objects.filter(telefono=telefono).exists():
                form.add_error('telefono', 'Este número de teléfono ya está registrado.')
                hay_duplicados = True
            if direccion and Empresa.objects.filter(direccion__iexact=direccion).exists():
                form.add_error('direccion', 'Esta dirección ya está registrada.')
                hay_duplicados = True

            if hay_duplicados:
                messages.error(request, 'No se pudo registrar la empresa debido a datos duplicados.')
            else:
                try:
                    form.save()
                    empresa_creada = True  # Marca que la empresa fue creada exitosamente
                except IntegrityError:
                    messages.error(request, 'Error: Ya existe una empresa registrada con ese Nombre o NIT.')
                except Exception as e:
                    messages.error(request, f'Error inesperado al guardar la empresa: {e}')
        else:
            messages.error(request, 'Por favor, corrige los errores indicados en el formulario.')
    else:
        form = EmpresaForm()

    context = {'form': form, 'empresa_creada': empresa_creada}
    return render(request, 'empresas/crear_empresa.html', context)

