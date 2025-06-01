from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

from tools.fishing_toolbox.base import phishing_ealvaradob
from tools.fishing_toolbox.translator import tralate_es_to_en
from tools.google_toolbox.tools_gmail import download_emails_as_html, gmail_get_message, search_message, send_draft, send_message
from tools.google_toolbox.utils import print_pretty_response

# LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001")

# Herramientas
tools = [send_draft, send_message, search_message, gmail_get_message, download_emails_as_html, phishing_ealvaradob, tralate_es_to_en]

content = "Eres un experto en detectar phishing en correos electrónicos. Siempre que te pregunten por correos, busca su ID, analiza su contenido, y determina si es phishing. Usa herramientas encadenadas si es necesario."


prompt = ChatPromptTemplate.from_messages([("system", "Eres un experto en detectar phishing en correos electrónicos. Usa herramientas para buscar correos, obtener contenido y determinar si son phishing."), ("user", "{input}"), MessagesPlaceholder(variable_name="agent_scratchpad")])


agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)
result = executor.invoke({"input": "¿Revisa mi ultimo correo y dime si es phishing y cual es su asunto?"})


print(result)
print_pretty_response(result)
