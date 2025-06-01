from pydantic import BaseModel
from typing import List, Dict, Optional
from enum import Enum

class Operator(Enum):
    FROM= "from"
    TO= "to"
    CC= "cc"
    BCC= "bcc"
    SUBJECT= "subject"
    HAS= "has"
    FILENAME= "filename"
    TEXTO= "texto"
    IN= "in"
    IS= "is"
    LABEL= "label"
    AFTER= "after"
    BEFORE= "before"
    OLDER_THAN= "older_than"
    NEWER_THAN= "newer_than"



class GmailStatusTools(Enum):
    ok= []


#  Por remitente o destinatario
# Operador	Ejemplo	Significado
# from:	from:juan@gmail.com	Correos enviados por esa persona
# to:	to:soporte@empresa.com	Correos enviados a esa persona
# cc:	cc:gerente@empresa.com	Enviados con copia a
# bcc:	bcc:secretaria@empresa.com	Enviados con copia oculta a

# 🧵 Por contenido o título
# Operador	Ejemplo	Significado
# subject:	subject:informe mensual	Busca en el asunto
# has:attachment	has:attachment	Correos con archivos adjuntos
# filename:	filename:pdf	Archivos adjuntos por tipo o nombre
# "texto"	"oferta exclusiva"	Frase exacta en el contenido

# 🗂️ Por carpeta, estado o etiqueta
# Operador	Ejemplo	Significado
# in:	in:inbox in:spam in:trash	En qué carpeta se encuentra
# is:	is:read, is:unread, is:starred	Estado del mensaje
# label:	label:importante	Mensajes con esa etiqueta

# ⏱️ Por fecha
# Operador	Ejemplo	Significado
# after:	after:2024/01/01	Después de esa fecha
# before:	before:2025/01/01	Antes de esa fecha
# older_than:	older_than:6m	Más antiguos que (d=días, m=meses)
# newer_than:	newer_than:1d	Más recientes que

# 💬 Por palabras
# Operador	Ejemplo	Significado
# -	-in:spam	Excluye (negación)
# OR	from:juan OR from:maria	Uno u otro
# AND (implícito)	from:juan has:attachment	Ambos criterios