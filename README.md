1. DESCRIPCIÓN DE LA IDEA DEL PROYECTO
Problema: Una empresa genera un volumen masivo de documentos diarios (historias laborales, comprobantes contables, facturas). Actualmente, existe una falta de control en el ciclo de vida del documento, dificultad para localizar expedientes físicos, riesgos de pérdida de información sensible y una comunicación ineficiente caracterizada por la pérdida de trazabilidad en los préstamos y la falta de un canal formal de comunicación entre el Archivo de Gestión (quien genera el dato) y el Archivo Central (quien custodia).
Solución: Un sistema web robusto que digitaliza el ciclo de vida del documento, permitiendo transferencias electrónicas y el control estricto de quién posee físicamente un expediente mediante Actas de Préstamo automáticas
2. OBJETIVO DEL SISTEMA
Desarrollar una plataforma integral de gestión documental que automatice el ciclo de vida de los documentos, desde su creación y digitalización en el archivo de gestión hasta su custodia definitiva en el archivo central, garantizando la trazabilidad de los préstamos físicos y el cumplimiento de las Tablas de Retención Documental (TRD).
3. USUARIOS DEL SISTEMA
•	Administrador: Gestiona usuarios, permisos, configuración de las TRD y auditoría global del sistema.

•	Usuario de Archivo de Gestión (Carga/Transferencia): Encargado de crear expedientes, solicitar préstamos y enviar transferencias documentales.


•	Usuario de Archivo Central (Revisión/Aprobación): Encargado de validar transferencias, aprobar o rechazar con comentarios, y controlar el inventario y retorno de documentos físicos.

4. FUNCIONES PRINCIPALES DEL SOFTWARE
•	 Gestión de Inventario (FUID): Módulo para el registro de carpetas con metadatos específicos (Cédula, Folios, Asunto).
•	Control de Préstamos Trazable: Registro obligatorio del usuario que solicita el documento para evitar pérdidas.
•	 Filtros de Seguridad: Personalización del panel administrativo para que cada usuario solo visualice lo que le corresponde según su rol.
•	Gestión de Tablas de Retención Documental (TRD): Creación y configuración de tiempos de retención y disposición final.
•	Carga y Visualización: Módulo para subir documentos digitales (PDF) y visualizarlos/descargarlos.
•	Flujo de Transferencias: Creación, revisión, comentarios y aprobación de transferencias entre archivos.
•	Control de Préstamos: Generación de actas digitales y seguimiento de estado (Prestado/Devuelto).
•	Módulo de Consultas: Notificaciones y solicitudes de búsqueda de documentos al Archivo Central.







5. DIAGRAMA DE CASOS DE USO
•	Archivo de Gestión: “Registrar", “Iniciar Sesión”, “Cargar Documento", "Crear Transferencia", "Solicitar Préstamo", Consultar estado.
•	Archivo Central: “Registrar", “Iniciar Sesión”, "Revisar Transferencia", "Aprobar / Rechazar Transferencia", "Gestionar Prestamos", “Registrar Devolución”.
•	Administrador: "Gestionar Usuarios", "Configurar Tablas de Retención Documental".




6. MODELO DE BASE DE DATOS


A. Tabla: Usuarios (Control de Acceso)
CAMPO	TIPO	DESCRIPCIÓN
ID_USUARIO	PK, INT	IDENTIFICADOR ÚNICO.
USERNAME	VARCHAR	NOMBRE DE USUARIO PARA EL LOGIN.
PASSWORD	VARCHAR	HASH DE LA CONTRASEÑA (SEGURIDAD).
ROL	ENUM	'ADMIN', 'ARCHIVO_GESTION', 'ARCHIVO_CENTRAL'.

B. Tabla: Documentos (Repositorio Principal)
CAMPO	TIPO	DESCRIPCIÓN
ID_DOC	PK, INT	IDENTIFICADOR DEL DOCUMENTO.
TITULO	VARCHAR	NOMBRE (EJ. "HISTORIA LABORAL - JUAN PÉREZ").
TIPO	ENUM	'CONTABLE', 'LABORAL'.
SUBTIPO	VARCHAR	'COMPROBANTE EGRESO', 'FACTURA', ETC.
RUTA_ARCHIVO	VARCHAR	LINK AL ARCHIVO DIGITALIZADO (PDF).
ESTADO_UBICACION	ENUM	'GESTION', 'CENTRAL'.
ID_TRANSFERENCIA	FK	RELACION CON TRANSFERENCIAS









C. Tabla: Transferencias (Flujo de Aprobación)
CAMPO	TIPO	DESCRIPCIÓN
ID_TRANS	PK, INT	ID DE LA TRANSFERENCIA.
ID_SOLICITANTE	FK	RELACIÓN CON USUARIOS (QUIEN CARGA).
ID_REVISOR	FK	RELACIÓN CON USUARIOS (QUIEN APRUEBA).
ESTADO	ENUM	'PENDIENTE', 'OBSERVADA', 'APROBADA'.
COMENTARIOS	TEXT	ESPACIO PARA CORRECCIONES.
ID_DOCUMENTO	FK	RELACION CON DOCUMENTOS
D. Tabla: Prestamos (Control de Físicos)
CAMPO	TIPO	DESCRIPCIÓN
ID_PRESTAMO	PK, INT	ID DEL ACTA DE PRÉSTAMO.
ID_DOC	FK	RELACIÓN CON DOCUMENTOS.
FECHA_SALIDA	DATETIME	CUANDO SALIÓ DEL ARCHIVO CENTRAL.
ESTADO_PRESTAMO	BOOLEAN	1 = PRESTADO, 0 = DEVUELTO.
ID_USUARIO_PIDE	FK	RELACION CON USUARIO

7. GESTIÓN DEL PROYECTO Y LA CONFIGURACIÓN
Gestión del Proyecto:
En lugar de encerrarnos 6 meses a programar y entregar todo al final (con el riesgo de que no sea lo que el cliente quería), se trabajara en ciclos de 2 semanas.
Entregas constantes: Cada 15 días se mostrará un avance real. Por ejemplo: "Hoy ya funciona el login", "Hoy ya se puede probar la seguridad".
Reuniones de equipo: Todos los días el equipo por medio de zoom se habla 15 minutos para saber si alguien está en dificultad con algo y ayudarlo.
Aprender sobre la marcha: Si el jefe de archivo ve algo que no le gusta en la primera semana, lo corregimos de inmediato. No esperamos al final
Aplicaría una metodología Ágil (Scrum), trabajando por "Sprints":
•	Sprint 1: Módulo de Login y Seguridad.
•	Sprint 2: Módulo de Carga y visualización de documentos.
•	Sprint 3: Flujo de Transferencias y Aprobaciones.
•	Sprint 4: Sistema de Préstamos y Reportes.
Gestión de la Configuración
Es el escudo que protege el programa para que nunca se pierda la información y siempre haya una copia de respaldo segura
Para asegurar que el software sea robusto y profesional, utilizaría:
1.	Control de Versiones: Git (GitHub/GitLab) Guardamos una copia de seguridad cada vez que hacemos un cambio importante, para gestionar el historial del código y permitir el trabajo en equipo
2.	Entornos de Despliegue: Separar los entornos de Desarrollo (pruebas internas), Pruebas/QA (donde los usuarios prueban el flujo de transferencia).
3.	Documentación Técnica: Registro de cambios en la base de datos y manuales de usuario según el rol (Gestión vs. Central).
