from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

from tools.fishing_toolbox.base import phishing_ealvaradob
from tools.fishing_toolbox.translator import translate_es_to_en
from tools.google_toolbox.tools_gmail import download_emails_as_html, gmail_get_message, search_message, send_draft, send_message

# Herramientas comunes
tools = [send_draft, send_message, search_message, gmail_get_message, download_emails_as_html, phishing_ealvaradob, translate_es_to_en]

# LLM común
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001", temperature=0)

# + Plan-and-Execute
system = """
        Eres un asistente experto en detectar phishing en correos electrónicos que sigue un proceso estructurado de planificación.

        ## PROCESO DE PLANIFICACIÓN OBLIGATORIO:

        ### 1. ANÁLISIS INICIAL
        Antes de usar cualquier herramienta, analiza la consulta del usuario y determina:
        - ¿Qué información específica necesitas obtener?
        - ¿Qué herramientas necesitarás usar y en qué orden?
        - ¿Hay dependencias entre las herramientas? (ej: necesitas un ID antes de obtener detalles)

        ### 2. PLAN DE EJECUCIÓN
        Crea un plan paso a paso que incluya:
        - Paso 1: [Herramienta] - [Propósito específico]
        - Paso 2: [Herramienta] - [Propósito específico]
        - Paso N: [Herramienta] - [Propósito específico]

        ### 3. EJECUCIÓN SECUENCIAL
        Ejecuta cada paso del plan y usa los resultados de herramientas anteriores para informar las siguientes:
        - Si una herramienta requiere un ID, primero usa search_message para obtenerlo
        - Si necesitas contenido completo, usa gmail_get_message con el ID obtenido
        - Si detectas posible phishing, usa phishing_ealvaradob para análisis detallado
        - Si hay texto en español, usa translate_es_to_en antes del análisis de phishing

        ### 4. RECOPILACIÓN COMPLETA DE INFORMACIÓN
        Para cada correo analizado, SIEMPRE proporciona:
        - Remitente (De:)
        - Destinatario (Para:)
        - Asunto
        - Fecha
        - Resumen del contenido
        - Análisis de phishing (si aplica)
        - Nivel de riesgo

        ## REGLAS ESPECÍFICAS:

        ✅ SIEMPRE busca IDs de correos antes de obtener detalles completos
        ✅ SIEMPRE usa herramientas en secuencia lógica (buscar → obtener → analizar)
        ✅ SIEMPRE completa información faltante usando las herramientas disponibles
        ✅ SIEMPRE analiza contenido sospechoso con herramientas de phishing
        ✅ SIEMPRE traduce texto en español antes de análisis de phishing
        ✅ COMBINA múltiples herramientas para obtener información completa

        ❌ NUNCA digas que no tienes acceso a una herramienta
        ❌ NUNCA omitas información que puedes obtener con las herramientas
        ❌ NUNCA uses herramientas sin un plan claro

        ## FORMATO DE RESPUESTA:
        1. **Plan de Acción**: [Describe tu plan paso a paso]
        2. **Ejecución**: [Usa las herramientas según el plan]
        3. **Resultados**: [Presenta información completa y análisis]
"""

def run_react_agent(input_text: str):
    agent = create_react_agent(llm, tools)
    # Prompt base para ReAct Agent (flexible)
    system_msg = SystemMessage(content=(system))
    user_message = HumanMessage(content=input_text)

    response = agent.invoke({"messages": [system_msg, user_message]})
    return response


def run_tool_calling_agent(input_text: str):
    # Prompt con agent_scratchpad obligatorio para Tool Calling Agent
    # prompt = ChatPromptTemplate.from_messages([("system", promt), ("user", "{input}"), MessagesPlaceholder(variable_name="agent_scratchpad")])

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )
    agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    response = executor.invoke({"input": input_text})

    # for step in executor.stream({"input": "tu consulta aquí"}):
    #     print(step)

    return response


def extecute(test_input: str):
    # print("==== ReAct Agent ====")
    # resp_react = run_react_agent(test_input)
    # print_pretty_response(resp_react)

    print("\n==== Tool Calling Agent ====")
    resp_tool_call = run_tool_calling_agent(test_input)
    # print(resp_tool_call)
    # print_pretty_response(resp_tool_call)

    return resp_tool_call


if __name__ == "__main__":
    test_input = "Revisa mi tercer correo y dime si es phishing"
    extecute(test_input)
