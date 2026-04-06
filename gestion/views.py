from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from datetime import datetime

# Librerías para generación de PDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from xhtml2pdf import pisa

# Importamos tus modelos
from .models import Prestamo, Transferencia, CarpetaTransferida

# --- 1. GENERAR ACTA DE PRÉSTAMO (Usando ReportLab) ---
def generar_pdf_prestamo(request, prestamo_id):
    from django.shortcuts import get_object_or_404
    # Esto busca el préstamo y si no existe da un error limpio, no un pantallazo amarillo
    # Obtenemos el préstamo o lanzamos 404 si no existe
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Acta_Prestamo_{prestamo.id}.pdf"'

    # Creamos el lienzo PDF
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # --- ENCABEZADO ---
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, height - 50, "SISTEMA DE GESTIÓN DOCUMENTAL")
    p.setFont("Helvetica-Bold", 12)
    p.drawCentredString(width / 2, height - 70, "ACTA DE PRÉSTAMO DE DOCUMENTOS")

    # --- CUERPO DEL DOCUMENTO ---
    p.setFont("Helvetica-Bold", 11)
    p.drawString(50, height - 120, "1. INFORMACIÓN DEL SOLICITANTE")
    p.setFont("Helvetica", 10)
    # Usamos get_full_name() si el usuario tiene nombre/apellido, sino su username
    nombre_usuario = prestamo.usuario.get_full_name() or prestamo.usuario.username
    p.drawString(70, height - 140, f"Usuario: {nombre_usuario}")
    p.drawString(70, height - 155, f"Fecha de Salida: {prestamo.fecha_salida}")

    p.setFont("Helvetica-Bold", 11)
    p.drawString(50, height - 190, "2. DETALLES DEL DOCUMENTO")
    p.setFont("Helvetica", 10)
    p.drawString(70, height - 210, f"Título: {prestamo.documento.titulo}")
    p.drawString(70, height - 225, f"Tipo de Documento: {prestamo.documento.tipo}")

    p.setFont("Helvetica-Bold", 11)
    p.drawString(50, height - 260, "3. OBSERVACIONES Y ESTADO")
    p.setFont("Helvetica", 10)
    
    # Manejo seguro de campos que podrían estar vacíos
    obs_general = getattr(prestamo, 'observaciones', "Sin observaciones adicionales.")
    obs_fisica = getattr(prestamo, 'observaciones_fisicas', "Estado físico no especificado.")
    
    p.drawString(70, height - 280, f"Observaciones Acta: {obs_general}")
    p.drawString(70, height - 295, f"Estado Físico: {obs_fisica}")

    # --- ESPACIO PARA FIRMAS ---
    p.line(50, 150, 250, 150)
    p.drawString(80, 135, "FIRMA ENTREGA")
    p.drawString(80, 120, "(Archivo de Gestión)")

    p.line(350, 150, 550, 150)
    p.drawString(380, 135, "FIRMA RECIBE")
    p.drawString(380, 120, "(Funcionario Solicitante)")

    # Finalizamos el PDF
    p.showPage()
    p.save()
    return response

# --- 2. EXPORTAR REPORTE FUID (Usando xhtml2pdf) ---
def exportar_fuid_pdf(request, transferencia_id):
    # Obtenemos la transferencia y sus carpetas relacionadas
    transferencia = get_object_or_404(Transferencia, id=transferencia_id)
    carpetas = transferencia.carpetas.all()
    
    context = {
        'transferencia': transferencia,
        'carpetas': carpetas,
        'fecha_actual': datetime.now(),
    }
    
    # Renderizamos el template HTML a un string
    # Asegúrate de tener este archivo en: templates/gestion/fuid_pdf.html
    html = render_to_string('gestion/fuid_pdf.html', context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="FUID_Transferencia_{transferencia.id}.pdf"'
    
    # Convertimos el HTML a PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse(f'Ocurrió un error al generar el FUID: {pisa_status.err}', status=500)
    
    return response