from django.urls import path
from . import views

app_name = 'admin_empresas'

urlpatterns = [
    path('', views.lista_empresas, name='lista_empresas'),
    path('editar/<int:empresa_id>/', views.editar_empresa, name='editar_empresa'),
    path('activar-desactivar/<int:empresa_id>/', views.toggle_estado_empresa, name='activar_desactivar_empresa'),
]
