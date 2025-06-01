from langchain_google_community.document_loaders.googledrive import get_google_credentials, build_resource_service



from googleapiclient.discovery import build

# Configurar credenciales con acceso de solo lectura
credentials = get_google_credentials(
    token_file="token.json",
    scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"],
    client_secrets_file="credentials.json",
)

# Construir el servicio de Sheets
service = build('sheets', 'v4', credentials=credentials)

# Leer datos de una hoja de cálculo
result = service.spreadsheets().values().get(
    spreadsheetId="ID_DE_TU_HOJA_DE_CALCULO",
    range="Hoja1!A1:D10"
).execute()