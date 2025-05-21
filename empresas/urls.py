from django.urls import path
from . import views
app_name = 'empresas'  # Nombre de la aplicación

urlpatterns = [
    path('crear/', views.crear_empresa, name='crear_empresa'),
    path('buscar/', views.listar_empresas, name='listar_empresas'), 
    # Nueva URL para los detalles de la empresa. <int:empresa_id> captura el ID como un entero
    path('<int:empresa_id>/', views.detalle_empresa, name='detalle_empresa'),
]