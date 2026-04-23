from django.urls import path
from . import views

urlpatterns = [
    # Ruta para el FUID (la que ya tenías)
    path('transferencia/<int:transferencia_id>/fuid/', views.exportar_fuid_pdf, name='pdf_fuid'),
    
    # NUEVA RUTA: Para el Acta de Préstamo (esto quita el error amarillo)
    path('prestamo/<int:prestamo_id>/pdf/', views.generar_pdf_prestamo, name='pdf_prestamo'),
]
from django.contrib import admin
from django.urls import path
from gestion import views # Importamos tus vistas

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'), # Página principal
]