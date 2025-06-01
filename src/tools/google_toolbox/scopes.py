from dotenv import load_dotenv

load_dotenv()

# https://mail.google.com/ #Todos los permisos
# https://www.googleapis.com/auth/gmail.readonly #- Solo lectura
# https://www.googleapis.com/auth/gmail.compose #- Crear mensajes y borradores
# https://www.googleapis.com/auth/gmail.send #- Enviar mensajes
# https://www.googleapis.com/auth/gmail.modify #- Todos los permisos excepto eliminar mensajes
SCOPES_GEMAIL= []

# https://www.googleapis.com/auth/calendar   # - Acceso completo (lectura/escritura)
# https://www.googleapis.com/auth/calendar.readonly   # - Solo lectura
# https://www.googleapis.com/auth/calendar.events # - Acceso a eventos (crear, editar, eliminar)
# https://www.googleapis.com/auth/calendar.events.readonly # - Solo lectura de eventos
# https://www.googleapis.com/auth/calendar.settings.readonly # - Solo lectura de configuraciones
# https://www.googleapis.com/auth/calendar.addons.execute # - Para complementos de Calendar
SCOPES_CALENDAR= []



# https://www.googleapis.com/auth/spreadsheets.readonly # Acceso de solo lectura a hojas de cálculo:
# https://www.googleapis.com/auth/spreadsheets #Acceso completo a hojas de cálculo
# https://www.googleapis.com/auth/drive.readonly  # Acceso de solo lectura a archivos en Google Drive (útil para listar hojas de cálculo)
SCOPES_SHEETS= []

SCOPES_DRIVE= []