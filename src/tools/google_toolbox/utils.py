from langchain_core.messages import BaseMessage
import base64


def decode_base64(data):
    decoded = base64.urlsafe_b64decode(data)
    try:
        return decoded.decode("utf-8")
    except UnicodeDecodeError:
        return decoded.decode("latin1")


def print_pretty_response(response: dict):
    from pprint import pprint

    print("===============================================")
    print("\n🧾 Resumen del flujo de mensajes:\n")
    for msg in response.get("messages", []):
        if isinstance(msg, BaseMessage):
            print(f"\n🔹 Tipo: {type(msg).__name__}")
            print(f"📜 Contenido:\n{msg.content}")
        elif isinstance(msg, dict):
            pprint(msg)
        else:
            print("\n🛑 Mensaje desconocido:\n")
            pprint(msg)



def extract_html_content(message):
    """Función auxiliar para extraer contenido HTML de un mensaje."""
    try:
        payload = message.get("payload", {})

        # Buscar en las partes del mensaje
        parts = payload.get("parts", [])

        for part in parts:
            if part.get("mimeType") == "text/html":
                data = part.get("body", {}).get("data", "")
                if data:
                    return decode_base64(data)

        # Si no hay partes, buscar en el cuerpo principal
        if payload.get("mimeType") == "text/html":
            data = payload.get("body", {}).get("data", "")
            if data:
                return decode_base64(data)

        # Fallback a texto plano
        for part in parts:
            if part.get("mimeType") == "text/plain":
                data = part.get("body", {}).get("data", "")
                if data:
                    text_content = decode_base64(data)
                    return f"<pre>{text_content}</pre>"

        return None

    except Exception:
        return None


