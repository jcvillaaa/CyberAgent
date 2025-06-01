import os
from typing import List


from langchain_core.tools import tool
from langchain_google_community.gmail.create_draft import GmailCreateDraft
from langchain_google_community.gmail.get_message import GmailGetMessage
from langchain_google_community.gmail.search import GmailSearch
from langchain_google_community.gmail.send_message import GmailSendMessage

from tools.google_toolbox.auth_gmail import AuthGmailToolKit
from tools.google_toolbox.utils import extract_html_content
# from auth_gmail import AuthGmailToolKit
# from utils import extract_html_content


gmail_tool_kit = AuthGmailToolKit()


@tool
def send_draft(message: str, to: List[str], subject: str) -> str:
    """Crear un borrador de correo electrónico en Gmail.

    Args:
        message: Contenido del mensaje
        to: Lista de destinatarios
        subject: Asunto del correo

    Returns:
        Mensaje de confirmación con el ID del borrador creado
    """
    print("Usando herramienta send_draft")
    try:
        toolkit = GmailCreateDraft(api_resource=gmail_tool_kit.api_resource)
        result = toolkit.invoke({
            "message": f"<b>{message}</b>",
            "to": to,
            "subject": subject
        })

        if "Draft created" in result:
            # Extraer ID del borrador de manera más robusta
            parts = result.split()
            if len(parts) >= 5:
                draft_id = parts[4]
                return f"✅ Borrador creado exitosamente. ID: {draft_id}"
            else:
                return f"✅ Borrador creado: {result}"
        else:
            return f"❌ Error al crear borrador: {result}"

    except Exception as e:
        return f"❌ Error inesperado al crear borrador: {str(e)}"


@tool
def send_message(message: str, to: List[str], subject: str) -> str:
    """Enviar un correo electrónico a través de Gmail.

    Args:
        message: Contenido del mensaje
        to: Lista de destinatarios
        subject: Asunto del correo

    Returns:
        Mensaje de confirmación con el ID del mensaje enviado
    """
    print("Usando herramienta send_message")
    try:
        toolkit = GmailSendMessage(api_resource=gmail_tool_kit.api_resource)
        result = toolkit.invoke({
            "message": f"<b>{message}</b>",
            "to": to,
            "subject": subject
        })

        if "Message sent" in result:
            # Extraer ID del mensaje de manera más robusta
            parts = result.split()
            if len(parts) >= 5:
                message_id = parts[4]
                return f"✅ Mensaje enviado exitosamente. ID: {message_id}"
            else:
                return f"✅ Mensaje enviado: {result}"
        else:
            return f"❌ Error al enviar mensaje: {result}"

    except Exception as e:
        return f"❌ Error inesperado al enviar mensaje: {str(e)}"


@tool
def search_message(query: str = "in:inbox", max_results: int = 3) -> str:
    """Buscar correos en Gmail usando operadores de búsqueda.

    Args:
        query: Consulta de búsqueda (ej: 'from:usuario@ejemplo.com', 'subject:importante')
        max_results: Número máximo de resultados a retornar

    Returns:
        Lista formateada de correos encontrados
    """
    print("Usando herramienta search_message")
    try:
        toolkit = GmailSearch(api_resource=gmail_tool_kit.api_resource)
        result = toolkit.invoke({
            "query": query,
            "max_results": max_results,
        })

        if not result:
            return f"📭 No se encontraron correos con la búsqueda: '{query}'"

        output = [f"🔍 Encontrados {len(result)} correos para '{query}':\n"]

        for i, mail in enumerate(result, 1):
            mail_info = f"""📧 Correo {i}:
                        • ID: {mail.get("id", "N/A")}
                        • De: {mail.get("sender", "No disponible")}
                        • Asunto: {mail.get("subject", "Sin asunto")}
                        • Vista previa: {mail.get("snippet", "Sin vista previa")}
                        • Thread ID: {mail.get("threadId", "N/A")}
                        • Fecha: {mail.get("internalDate", "Sin fecha")}"""

            output.append(mail_info)

        return "\n\n".join(output)

    except Exception as e:
        return f"❌ Error al buscar correos: {str(e)}"


@tool
def gmail_get_message(ID: str) -> str:
    """Obtener los detalles completos de un mensaje de Gmail.

    Args:
        ID: ID del mensaje a obtener

    Returns:
        Detalles formateados del mensaje incluyendo contenido y adjuntos
    """
    print("Usando herramienta gmail_get_message")
    try:
        toolkit = GmailGetMessage(api_resource=gmail_tool_kit.api_resource)
        message = toolkit.invoke(ID) # {'id': '197290fd63bc3362', 'threadId': '197290fd63bc3362', 'snippet': 'Hola mundo', 'body': '', 'subject': 'mensaje de test langchain', 'sender': 'juancamilovillaagudelo@gmail.com'}

        id= message.get("id", "No disponible")
        threadId= message.get("threadId", "No disponible")
        snippet= message.get("snippet", "No disponible")
        body= message.get("body", "No disponible")
        subject= message.get("subject", "No disponible")
        sender= message.get("sender", "No disponible")


        attachments = message.get("attachments", [])

        summary = f"""📩 Detalles del correo (ID: {id}):
                   threadId: {threadId}
                   snippet: {snippet}
                📤 De: {sender}
                📋 Asunto: {subject}
                📝 Contenido:
                {body}"""

        if attachments:
            summary += "\n\n📎 Adjuntos:"
            for i, attachment in enumerate(attachments, 1):
                summary += f"\n   {i}. {attachment.get('filename', 'Sin nombre')} ({attachment.get('mime_type', 'Tipo desconocido')}, {attachment.get('size', 0)} bytes)"
        else:
            summary += "\n\n📎 Sin adjuntos"

        return summary

    except Exception as e:
        return f"❌ Error al obtener mensaje {ID}: {str(e)}"


@tool
def download_emails_as_html(query: str = "from:platzi", max_results: int = 3) -> str:
    """Buscar correos y descargarlos como archivos HTML.

    Args:
        query: Consulta de búsqueda para encontrar correos
        max_results: Número máximo de correos a descargar

    Returns:
        Lista de archivos HTML creados o mensaje de error
    """
    print("Usando herramienta download_emails_as_html")
    try:
        # Usar la API directamente para mayor control
        service = gmail_tool_kit.api_resource

        # Crear directorio si no existe
        os.makedirs("correos_html", exist_ok=True)

        # Buscar mensajes
        results = service.users().messages().list(
            userId="me",
            q=query,
            maxResults=max_results
        ).execute()

        messages = results.get("messages", []) # [{'id': '197238f374bb7558', 'threadId': '197238f374bb7558'}, {'id': '196ee6f3ba126404', 'threadId': '196ee6f3ba126404'}, {'id': '196c6dab2cbb5d7d', 'threadId': '196c6dab2cbb5d7d'}]

        if not messages:
            return f"📭 No se encontraron correos para la consulta: '{query}'"

        saved_files = []
        failed_downloads = []

        for msg in messages:
            msg_id = msg["id"]
            try:
                # Obtener mensaje completo
                message = service.users().messages().get(
                    userId="me",
                    id=msg_id,
                    format="full"
                ).execute()

                # Extraer contenido HTML
                html_content = extract_html_content(message)

                if html_content:
                    # Guardar como archivo HTML
                    filename = f"correos_html/{msg_id}.html"
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(html_content)
                    saved_files.append(filename)
                else:
                    failed_downloads.append(msg_id)

            except Exception as e:
                failed_downloads.append(f"{msg_id} (Error: {str(e)})")

        # Preparar respuesta
        result_parts = []

        if saved_files:
            result_parts.append(f"✅ {len(saved_files)} correos descargados exitosamente:")
            for file in saved_files:
                result_parts.append(f"   • {file}")

        if failed_downloads:
            result_parts.append(f"\n❌ {len(failed_downloads)} correos fallaron:")
            for failed in failed_downloads:
                result_parts.append(f"   • {failed}")

        if not saved_files and not failed_downloads:
            return "📭 No se encontró contenido descargable en los correos."

        return "\n".join(result_parts)

    except Exception as e:
        return f"❌ Error al descargar correos: {str(e)}"




if __name__ == "__main__":
    message = "Hola mundo"
    to = ["juancamilovillaagudelo@gmail.com"]
    subject= "mensaje de test langchain"
    # result = send_draft(message, to, subject) # 197290fd63bc3362, 197290fda1ab16c9, 197290e533f2d4c5, 19728ed1733d636c
    #result= send_message(message, to, subject)
    #result= search_message()
    result = gmail_get_message("197290fd63bc3362")
    #result= download_emails_as_html()
    print(result)
