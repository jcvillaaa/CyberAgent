import langchain
from agents.cyber_agent.run_agent import extecute

print(langchain.__version__)


test_input = "Revisa mi ultimo correo e identifica si es phishing"
test_input = "cual es mi ultimo correo"
test_input= "envia un mensaje a juancamilovillaagudelo@gmail.com agreadeciendo por el almuerzo, se emotivo"
test_input= "revisa mi ultimo correo de platzi y dime si es phishing"
test_input= "Descarga mi ultimo correo de langchain en html"
result= extecute(test_input)
print("======================")
print(result.get("output"))
