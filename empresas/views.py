from django.shortcuts import render, redirect
from .forms import EmpresaForm


# Create your views here.

def crear_empresa(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crear_empresa')  # Redirige a la misma página o a otra según sea necesario
    else:
        form = EmpresaForm()
    return render(request, 'empresas/crear_empresa.html', {'form': form})