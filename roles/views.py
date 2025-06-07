from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from .models import Roles
from .forms import RolPermisosForm
from django.urls import reverse

@login_required
@permission_required('usuarios.puede_gestionar_usuarios', raise_exception=True)
def listar_roles(request):
    roles = Roles.objects.all()
    return render(request, 'roles/listar_roles.html', {'roles': roles})

@login_required
@permission_required('usuarios.puede_gestionar_usuarios', raise_exception=True)
def crear_rol(request):
    if request.method == 'POST':
        form = RolPermisosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('roles:listar_roles')
    else:
        form = RolPermisosForm()
    return render(request, 'roles/crear_rol.html', {'form': form})

@login_required
@permission_required('usuarios.puede_gestionar_usuarios', raise_exception=True)
def editar_rol(request, rol_id):
    rol = get_object_or_404(Roles, id_rol=rol_id)
    if request.method == 'POST':
        form = RolPermisosForm(request.POST, instance=rol)
        if form.is_valid():
            form.save()
            return redirect('roles:listar_roles')
    else:
        form = RolPermisosForm(instance=rol)
    return render(request, 'roles/editar_rol.html', {'form': form, 'rol': rol})

@login_required
@permission_required('usuarios.puede_gestionar_usuarios', raise_exception=True)
def eliminar_rol(request, rol_id):
    rol = get_object_or_404(Roles, id_rol=rol_id)
    if request.method == 'POST':
        rol.delete()
        return redirect('roles:listar_roles')
    return render(request, 'roles/eliminar_rol_confirmar.html', {'rol': rol})
