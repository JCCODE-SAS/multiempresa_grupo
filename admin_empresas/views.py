from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from empresas.models import Empresa

def lista_empresas(request):
    empresas = Empresa.objects.all()
    return render(request, 'admin_empresas/lista_empresas.html', {'empresas': empresas})

@login_required
def editar_empresa(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    cambio_exitoso = False  # Variable para controlar el mensaje de éxito

    if request.method == 'POST':
        # Actualizar los datos de la empresa
        empresa.nombre = request.POST.get('nombre')
        empresa.nit = request.POST.get('nit')
        empresa.correo_corporativo = request.POST.get('correo')
        empresa.telefono = request.POST.get('telefono')
        empresa.direccion = request.POST.get('direccion')
        empresa.pais = request.POST.get('pais')
        empresa.usuario_editor = request.user  # Registrar el usuario que edita
        empresa.save()
        cambio_exitoso = True  # Indicar que el cambio fue exitoso

    return render(request, 'admin_empresas/editar_empresa.html', {'empresa': empresa, 'cambio_exitoso': cambio_exitoso})

def toggle_estado_empresa(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    empresa.is_active = not empresa.is_active # Asegúrate de tener un campo booleano `activa`
    empresa.save()
    return redirect('admin_empresas:lista_empresas')
