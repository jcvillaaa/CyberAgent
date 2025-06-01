¡Excelente iniciativa! Vamos a dominar estas herramientas de Gmail en `langchain_google_community` como un verdadero 🧙‍♂️ mago del código.

---

## 🧩 Herramientas de Gmail disponibles

Estas 5 clases son **herramientas LangChain integradas** sobre la API de Gmail. Usan `api_resource` (instancia de `googleapiclient.discovery.Resource`) para operar.

---

### 1. `GmailCreateDraft`

📝 Crea un **borrador de correo**.

#### 📌 Parámetros:

* `to` (str): dirección de correo del destinatario
* `subject` (str): asunto
* `body` (str): contenido HTML o texto

#### 🧪 Ejemplo:

```python
from langchain_google_community.gmail.create_draft import GmailCreateDraft

tool = GmailCreateDraft(api_resource=api_resource)
tool.invoke({
    "to": "destino@ejemplo.com",
    "subject": "¡Hola desde LangChain!",
    "body": "<b>Esto es un borrador creado por código</b>"
})
```

---

### 2. `GmailSendMessage`

📤 Envía un **correo electrónico directo** (sin borrador).

#### 📌 Parámetros:

* `to` (str): destino
* `subject` (str): asunto
* `body` (str): contenido del correo (HTML o texto)

#### 🧪 Ejemplo:

```python
from langchain_google_community.gmail.send_message import GmailSendMessage

tool = GmailSendMessage(api_resource=api_resource)
tool.invoke({
    "to": "destino@ejemplo.com",
    "subject": "Correo enviado!",
    "body": "Este mensaje fue enviado desde Python usando LangChain."
})
```

---

### 3. `GmailSearch`

🔍 Busca mensajes en Gmail según una query.

#### 📌 Parámetros:

* `query` (str): ej. `"from:platzi.com"`
* `max_results` (int): número máximo de correos
* `resource` (str): `"messages"` o `"threads"`

#### 🧪 Ejemplo:

```python
from langchain_google_community.gmail.search import GmailSearch

tool = GmailSearch(api_resource=api_resource)
resultados = tool.invoke({
    "query": "in:inbox newer_than:7d",
    "max_results": 5,
    "resource": "messages"
})
print(resultados)
```

---

### 4. `GmailGetMessage`

📨 Obtiene un correo por ID.

#### 📌 Parámetros:

* `message_id` (str): ID del mensaje (obtenido con `GmailSearch`)

#### 🧪 Ejemplo:

```python
from langchain_google_community.gmail.get_message import GmailGetMessage

tool = GmailGetMessage(api_resource=api_resource)
mensaje = tool.invoke({"message_id": "17f3b4f9a8b4cdd4"})
print(mensaje["snippet"])
```

---

### 5. `GmailGetThread`

🧵 Recupera un **hilo de conversación completo**.

#### 📌 Parámetros:

* `thread_id` (str): ID del hilo

#### 🧪 Ejemplo:

```python
from langchain_google_community.gmail.get_thread import GmailGetThread

tool = GmailGetThread(api_resource=api_resource)
hilo = tool.invoke({"thread_id": "17f3b4f9a8b4cdd4"})
for mensaje in hilo["messages"]:
    print(mensaje["snippet"])
```

---

¿Te gustaría que los empaquete en una interfaz CLI, GUI, o agente LangChain interactivo?

Hotkeys:

* D ⚙️ Convierte estas funciones en un CLI interactivo
* V ✂️ Refactoriza en módulos: draft.py, send.py, etc.
* E 🧱 Integra todos como herramientas para un agente
* S 📖 Explica cómo autenticar con otros scopes o cuentas



---

Gmail utiliza su propio sistema de *operadores de búsqueda* para filtrar correos, muy similar a cómo funciona en su interfaz web. Estos filtros pueden combinarse con lógica booleana y permiten búsquedas muy específicas.

---

### 🧰 **Principales Filtros de Búsqueda Gmail**

#### 🧍‍♂️ Por remitente o destinatario

| Operador | Ejemplo                      | Significado                      |
| -------- | ---------------------------- | -------------------------------- |
| `from:`  | `from:juan@gmail.com`        | Correos enviados por esa persona |
| `to:`    | `to:soporte@empresa.com`     | Correos enviados a esa persona   |
| `cc:`    | `cc:gerente@empresa.com`     | Enviados con copia a             |
| `bcc:`   | `bcc:secretaria@empresa.com` | Enviados con copia oculta a      |

#### 🧵 Por contenido o título

| Operador         | Ejemplo                   | Significado                         |
| ---------------- | ------------------------- | ----------------------------------- |
| `subject:`       | `subject:informe mensual` | Busca en el asunto                  |
| `has:attachment` | `has:attachment`          | Correos con archivos adjuntos       |
| `filename:`      | `filename:pdf`            | Archivos adjuntos por tipo o nombre |
| `"texto"`        | `"oferta exclusiva"`      | Frase exacta en el contenido        |

#### 🗂️ Por carpeta, estado o etiqueta

| Operador | Ejemplo                              | Significado                 |
| -------- | ------------------------------------ | --------------------------- |
| `in:`    | `in:inbox` `in:spam` `in:trash`      | En qué carpeta se encuentra |
| `is:`    | `is:read`, `is:unread`, `is:starred` | Estado del mensaje          |
| `label:` | `label:importante`                   | Mensajes con esa etiqueta   |

#### ⏱️ Por fecha

| Operador      | Ejemplo             | Significado                        |
| ------------- | ------------------- | ---------------------------------- |
| `after:`      | `after:2024/01/01`  | Después de esa fecha               |
| `before:`     | `before:2025/01/01` | Antes de esa fecha                 |
| `older_than:` | `older_than:6m`     | Más antiguos que (d=días, m=meses) |
| `newer_than:` | `newer_than:1d`     | Más recientes que                  |

#### 💬 Por palabras

| Operador          | Ejemplo                    | Significado        |
| ----------------- | -------------------------- | ------------------ |
| `-`               | `-in:spam`                 | Excluye (negación) |
| `OR`              | `from:juan OR from:maria`  | Uno u otro         |
| `AND` (implícito) | `from:juan has:attachment` | Ambos criterios    |

---

### 🔀 **Combinaciones Poderosas**

```text
from:facturacion@empresa.com subject:factura has:attachment after:2024/01/01
```

```text
label:trabajo is:unread -in:spam
```

```text
from:(juan OR maria) subject:(reporte mensual) newer_than:10d
```

---

### 📜 Tips

* Fechas deben ir en formato `AAAA/MM/DD`
* Usa comillas para búsquedas exactas de frases
* Los operadores pueden anidarse o repetirse

¿Quieres que cree una función para construir estas búsquedas automáticamente con parámetros en Python?

Hotkeys:

* D ⚙️ Generar builder Python para filtros
* T 🧪 Test con filtros reales y GmailSearch
* V 🔎 Separar filtros útiles por caso de uso
* S 📘 Explicación paso a paso de filtros clave
