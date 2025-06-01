# from langchain_core.tools import tool
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# tokenizer  = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-es-en")
# model  = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-es-en")

# @tool
# def tralate_es_to_en(text: str) -> str:
#     """Traduce texto del idioma español al ingles"""
#     input= tokenizer(text, return_tensors="pt", padding=True)
#     output= model.generate(**input)
#     result = tokenizer.batch_decode(output, skip_special_tokens=True)
#     return result


# if __name__ == "__main__":

#     text= "Hola Mundo"

#     result= tralate_es_to_en(text)
#     print(result)

#     traslator = pipeline("translation_es_to_en", model="Helsinki-NLP/opus-mt-es-en")
#     print(traslator(text))

from langchain_core.tools import tool
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

# Cargar modelo una sola vez
tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-es-en")
model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-es-en")


@tool
def translate_es_to_en(text: str) -> str:
    """Traduce texto del idioma español al inglés usando el modelo Helsinki-NLP.

    Args:
        text: Texto en español a traducir

    Returns:
        Texto traducido al inglés en formato legible
    """
    print("Usando herramienta translate_es_to_en")
    try:
        # Validar entrada
        if not text or not text.strip():
            return "❌ Error: El texto no puede estar vacío"

        # Procesar con el modelo
        input_tokens = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        output = model.generate(**input_tokens, max_length=512, num_beams=4, early_stopping=True)
        result = tokenizer.batch_decode(output, skip_special_tokens=True)

        # Extraer la traducción (tomar el primer resultado)
        traduccion = result[0] if result else "No se pudo generar traducción"

        resultado_formateado = f"""🔄 Traducción Español → Inglés

📝 Texto original: "{text}"
🎯 Traducción: "{traduccion}"
🤖 Modelo: Helsinki-NLP/opus-mt-es-en
"""

        return resultado_formateado

    except Exception as e:
        return f"❌ Error al traducir: {str(e)}"


@tool
def translate_es_to_en_pipeline(text: str) -> str:
    """Traduce texto del español al inglés usando pipeline de transformers.

    Args:
        text: Texto en español a traducir

    Returns:
        Texto traducido al inglés usando pipeline optimizado
    """
    try:
        # Validar entrada
        if not text or not text.strip():
            return "❌ Error: El texto no puede estar vacío"

        # Crear pipeline (idealmente esto debería estar fuera para reutilización)
        translator = pipeline("translation", model="Helsinki-NLP/opus-mt-es-en")

        # Procesar traducción
        result = translator(text, max_length=512)

        if not result or len(result) == 0:
            return "❌ Error: No se pudo procesar la traducción"

        # Extraer traducción
        traduccion = result[0]["translation_text"]
        score = result[0].get("score", 0.0)

        resultado_formateado = f"""🔄 Traducción Español → Inglés (Pipeline)

📝 Texto original: "{text}"
🎯 Traducción: "{traduccion}"
📊 Confianza: {score:.2f}
🤖 Modelo: Helsinki-NLP/opus-mt-es-en
"""

        return resultado_formateado

    except Exception as e:
        return f"❌ Error al traducir con pipeline: {str(e)}"


@tool
def translate_batch_es_to_en(texts: str) -> str:
    """Traduce múltiples textos del español al inglés separados por líneas.

    Args:
        texts: Textos en español separados por saltos de línea

    Returns:
        Traducciones correspondientes en formato legible
    """
    try:
        # Validar entrada
        if not texts or not texts.strip():
            return "❌ Error: Los textos no pueden estar vacíos"

        # Dividir textos por líneas
        text_list = [line.strip() for line in texts.split("\n") if line.strip()]

        if not text_list:
            return "❌ Error: No se encontraron textos válidos para traducir"

        # Crear pipeline
        translator = pipeline("translation", model="Helsinki-NLP/opus-mt-es-en")

        # Procesar traducciones
        results = translator(text_list, max_length=512)

        # Formatear resultados
        output_lines = ["🔄 Traducción por lotes Español → Inglés\n"]

        for i, (original, result) in enumerate(zip(text_list, results), 1):
            traduccion = result["translation_text"]
            output_lines.append(f"""📝 Texto {i}:
   Original: "{original}"
   Traducción: "{traduccion}"
""")

        output_lines.append("🤖 Modelo: Helsinki-NLP/opus-mt-es-en")
        output_lines.append(f"📊 Total procesado: {len(text_list)} textos")

        return "\n".join(output_lines)

    except Exception as e:
        return f"❌ Error al traducir por lotes: {str(e)}"
