from django.urls import path
from . import views
app_name = 'empresas'  # Nombre de la aplicación

urlpatterns = [
    path('crear/', views.crear_empresa, name='crear_empresa'),
    path('listar/', views.listar_empresas, name='listar_empresas'),
    path('<int:empresa_id>/detalle/', views.detalle_empresa, name='detalle_empresa'),
    path('<int:pk>/historial/', views.historial_actividad, name='historial_actividad'),
]