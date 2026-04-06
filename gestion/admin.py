from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Documento, Prestamo, Transferencia, CarpetaTransferida

# --- DOCUMENTOS ---
@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'estado')
    search_fields = ('titulo',)

# --- PRÉSTAMOS ---
@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    # 'usuario' solo funcionará después del comando 'migrate'
    list_display = ('id', 'documento', 'usuario', 'fecha_salida', 'acciones_pdf')
    search_fields = ('usuario__username', 'documento__titulo')

    def acciones_pdf(self, obj):
        try:
            url = reverse('pdf_prestamo', args=[obj.id])
            return format_html(
                '<a class="button" href="{}" target="_blank" '
                'style="background-color: #417690; color: white; padding: 5px 10px; '
                'border-radius: 4px; text-decoration: none;">Imprimir Acta</a>', url
            )
        except:
            return "Error en URL"

# --- TRANSFERENCIAS (Allison puede crear carpetas aquí) ---
class CarpetaInline(admin.TabularInline):
    model = CarpetaTransferida
    extra = 1
    # CAMBIO: Usamos 'nombre_carpeta' porque 'asunto' no existe en tu modelo
    fields = ('cedula', 'nombre', 'apellido', 'nombre_carpeta', 'folios', 'estado')

@admin.register(Transferencia)
class TransferenciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario_gestion', 'estado', 'fecha_creacion', 'reporte_pdf')
    inlines = [CarpetaInline]

    def reporte_pdf(self, obj):
        try:
            url = reverse('pdf_fuid', args=[obj.id])
            return format_html('<a class="button" href="{}" target="_blank" style="background-color: #28a745; color: white; padding: 5px 10px; border-radius: 4px;">PDF FUID</a>', url)
        except:
            return "Sin URL"
        

# Al final de tu gestion/admin.py
admin.site.site_header = "Sistema de Gestión Documental"
admin.site.site_title = "Panel de Control SGD"
admin.site.index_title = "Bienvenido al Sistema de Gestión Documental"