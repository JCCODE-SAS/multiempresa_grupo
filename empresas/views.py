from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib import messages
from .forms import EmpresaForm
from .models import Empresa
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required # Importar el decorador
from django.db.models import Q # Importa Q para búsquedas complejas

@login_required # Asegura que solo usuarios autenticados puedan acceder a esta vista
def crear_empresa(request):
    empresa_creada = False  # Variable para controlar si se muestra el modal
    empresa_creada = False  # Variable para controlar si se muestra el modal
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('correo_corporativo')
            telefono = form.cleaned_data.get('telefono')
            direccion = form.cleaned_data.get('direccion')

            hay_duplicados = False

            # Validaciones personalizadas de duplicados
            if email and Empresa.objects.filter(correo_corporativo__iexact=email).exists():
                form.add_error('correo_corporativo', 'Este correo electrónico ya está registrado.')
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
                    empresa = form.save(commit=False)
                    empresa.usuario_creador = request.user  # Asignar el usuario creador
                    empresa.save()  # Guardar la empresa en la base de datos
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

@login_required
def listar_empresas(request):
    """
    Vista para mostrar la lista de empresas con opción de búsqueda por nombre.
    """
    empresas = Empresa.objects.all().order_by('nombre') # Obtiene todas las empresas inicialmente
    query = request.GET.get('q') # Obtiene el término de búsqueda del parámetro 'q' en la URL

    if query:
        # Filtra las empresas cuyo nombre contenga el término de búsqueda (insensible a mayúsculas/minúsculas)
        empresas = empresas.filter(nombre__icontains=query)

    context = {
        'empresas': empresas,
        'query': query # Pasamos el término de búsqueda al template para mantenerlo en la barra
    }
    # Seguimos usando el mismo template por ahora, pero lo modificaremos
    return render(request, 'empresas/listar_empresas.html', context)

@login_required
def detalle_empresa(request, empresa_id):
    """
    Vista para mostrar los detalles de una empresa específica.
    """
    # Intenta obtener la empresa por su ID, si no existe, devuelve un error 404
    empresa = get_object_or_404(Empresa, pk=empresa_id)
    context = {
        'empresa': empresa
    }
    return render(request, 'empresas/detalle_empresa.html', context) # Usaremos un nuevo template aquí