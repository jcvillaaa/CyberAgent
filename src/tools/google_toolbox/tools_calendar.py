from langchain_google_community import CalendarToolkit

toolkit = CalendarToolkit()

from langchain_google_community import CalendarToolkit
from langchain_google_community.calendar.utils import (
    build_resource_service,
    get_google_credentials,
)

# Puedes revisar los alcances en: https://developers.google.com/calendar/api/auth
credentials = get_google_credentials(
    token_file="token.json",
    scopes=["https://www.googleapis.com/auth/calendar"],
    client_secrets_file="credentials.json",
)

api_resource = build_resource_service(credentials=credentials)
toolkit = CalendarToolkit(api_resource=api_resource)

# CalendarCreateEvent: Crear eventos en el calendario
# CalendarSearchEvents: Buscar eventos
# CalendarUpdateEvent: Actualizar eventos existentes
# GetCalendarsInfo: Obtener información de los calendarios
# CalendarMoveEvent: Mover eventos entre calendarios
# CalendarDeleteEvent: Eliminar eventos
# GetCurrentDatetime: Obtener la fecha y hora actual


from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

# Crear el modelo de chat
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001")

# Obtener las herramientas de Google Calendar
calendar_tools = toolkit.get_tools()

# Crear un agente que use el modelo y las herramientas
agent_executor = create_react_agent(llm, calendar_tools)




example_query = "Crea un evento verde para 12/05/2025 18:00:00 hora colombia, para salir a correr durante 30 minutos."

events = agent_executor.stream(
    {"messages": [("user", example_query)]},
    stream_mode="values",
)
for event in events:
    event["messages"][-1].pretty_print()



{
        "summary": "Calculus exam",
        "start_datetime": "2025-07-11 11:00:00",
        "end_datetime": "2025-07-11 13:00:00",
        "timezone": "America/Mexico_City",
        "location": "UAM Cuajimalpa",
        "description": "Event created from the LangChain toolkit",
        "reminders": [{"method": "popup", "minutes": 60}],
        "conference_data": True,
        "color_id": "5",
    }




