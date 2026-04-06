from django.db import models
from django.contrib.auth.models import User

# --- 1. MODELO: DOCUMENTOS ---
class Documento(models.Model):
    ESTADOS = [
        ('G', 'En Archivo de Gestión'),
        ('P', 'Transferencia Pendiente'),
        ('C', 'Aceptado en Archivo Central'),
        ('R', 'Rechazado'),
    ]
    
    titulo = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='documentos/', blank=True, null=True) 
    tipo = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=1, choices=ESTADOS, default='G')
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.titulo

# --- 2. MODELO: PRÉSTAMOS ---
class Prestamo(models.Model):
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) # Este es el campo que causaba el error de columna
    fecha_salida = models.DateField(auto_now_add=True)
    devuelto = models.BooleanField(default=False)
    
    # Campos para la gestión digital y física
    archivo_digital = models.FileField(
        upload_to='prestamos/digital/', 
        null=True, 
        blank=True, 
        verbose_name="Documento Digitalizado"
    )
    observaciones_fisicas = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Notas del estado físico"
    )
    # Campo para las observaciones que aparecen en el Acta PDF
    observaciones = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Observaciones del Acta"
    )

    def __str__(self):
        return f"Préstamo {self.id} - {self.documento.titulo}"

# --- 3. MODELO: TRANSFERENCIAS (PAQUETE) ---
class Transferencia(models.Model):
    ESTADOS_TRANS = [
        ('creacion', 'En Creación'),
        ('enviada', 'Enviada a Central'),
        ('finalizada', 'Finalizada'),
    ]
    
    usuario_gestion = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transferencias_enviadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_TRANS, default='creacion')

    def __str__(self):
        return f"Transferencia {self.id} - {self.usuario_gestion.username}"

# --- 4. MODELO: CARPETAS (DETALLE DE LA TRANSFERENCIA) ---
class CarpetaTransferida(models.Model):
    ESTADOS_CARPETA = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]
    
    transferencia = models.ForeignKey(Transferencia, on_delete=models.CASCADE, related_name='carpetas')
    
    # Datos que pide el FUID
    cedula = models.CharField(max_length=20, verbose_name="Cédula/ID")
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    
    # IMPORTANTE: Este nombre es el que debe ir en el admin.py
    nombre_carpeta = models.CharField(max_length=255, verbose_name="Asunto/Título")
    
    folios = models.PositiveIntegerField(default=0, verbose_name="Folios")
    estado = models.CharField(max_length=20, choices=ESTADOS_CARPETA, default='pendiente')
    comentarios_central = models.TextField(blank=True, null=True, verbose_name="Observaciones Central")

    def __str__(self):
        return f"{self.cedula} - {self.nombre_carpeta}"