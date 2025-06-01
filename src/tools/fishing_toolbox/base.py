from langchain_core.tools import tool
from torch import argmax
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

# Cargar modelos una sola vez
tokenizer_phishing = AutoTokenizer.from_pretrained("ealvaradob/bert-finetuned-phishing")
model_ealvaradob = AutoModelForSequenceClassification.from_pretrained("ealvaradob/bert-finetuned-phishing")
model_elslay = pipeline("text-classification", model="ElSlay/BERT-Phishing-Email-Model")


@tool
def phishing_ealvaradob(text: str) -> str:
    """Analiza si un texto es phishing usando el modelo BERT de ealvaradob.

    Args:
        text: Texto a analizar (email, URL, SMS o cualquier texto)

    Returns:
        Análisis de phishing con predicción y nivel de confianza en formato legible
    """
    print("Usando herramienta phishing_ealvaradob")
    try:
        # Validar entrada
        if not text or not text.strip():
            return "❌ Error: El texto no puede estar vacío"

        # Procesar con el modelo
        input_tokens = tokenizer_phishing(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        output = model_ealvaradob(**input_tokens)
        logits = output.logits
        probabilidades = logits.softmax(dim=1)
        prediccion_id = argmax(probabilidades, dim=1)

        # Extraer resultado
        pred_id = prediccion_id[0].item()
        etiqueta_predicha = model_ealvaradob.config.id2label[pred_id]
        prob_predicha = probabilidades[0, pred_id].item()

        # Determinar clasificación
        es_phishing = etiqueta_predicha == "phishing"
        clasificacion = "🚨 PHISHING" if es_phishing else "✅ BENIGNO"
        confianza = prob_predicha * 100

        # Determinar nivel de riesgo
        if es_phishing:
            if confianza >= 90:
                nivel_riesgo = "MUY ALTO"
            elif confianza >= 70:
                nivel_riesgo = "ALTO"
            else:
                nivel_riesgo = "MODERADO"
        else:
            nivel_riesgo = "BAJO"

        resultado = f"""🔍 Análisis de Phishing (Modelo: ealvaradob/BERT)

                        📊 Resultado: {clasificacion}
                        🎯 Confianza: {confianza:.1f}%
                        ⚠️ Nivel de Riesgo: {nivel_riesgo}

                        📝 Texto analizado: "{text[:100]}{'...' if len(text) > 100 else ''}"
                    """

        return resultado

    except Exception as e:
        return f"❌ Error al analizar con modelo ealvaradob: {str(e)}"


@tool
def phishing_elslay(text: str) -> str:
    """Analiza si un texto es phishing usando el modelo BERT de ElSlay.

    Args:
        text: Texto a analizar (email, URL, SMS o cualquier texto)

    Returns:
        Análisis de phishing con predicción y nivel de confianza en formato legible
    """
    print("Usando herramienta phishing_elslay")
    try:
        # Validar entrada
        if not text or not text.strip():
            return "❌ Error: El texto no puede estar vacío"

        # Procesar con el modelo
        resultado = model_elslay(text)

        if not resultado or len(resultado) == 0:
            return "❌ Error: No se pudo procesar el texto"

        # Extraer resultado (tomar el primer resultado si hay múltiples)
        pred_info = resultado[0]
        pred_id = pred_info["label"]
        prob_predicha = pred_info["score"]

        # Determinar clasificación
        es_phishing = pred_id == "LABEL_1"
        clasificacion = "🚨 PHISHING" if es_phishing else "✅ BENIGNO"
        confianza = prob_predicha * 100

        # Determinar nivel de riesgo
        if es_phishing:
            if confianza >= 90:
                nivel_riesgo = "MUY ALTO"
            elif confianza >= 70:
                nivel_riesgo = "ALTO"
            else:
                nivel_riesgo = "MODERADO"
        else:
            nivel_riesgo = "BAJO"

        resultado_formateado = f"""🔍 Análisis de Phishing (Modelo: ElSlay/BERT)

📊 Resultado: {clasificacion}
🎯 Confianza: {confianza:.1f}%
⚠️ Nivel de Riesgo: {nivel_riesgo}

📝 Texto analizado: "{text[:100]}{'...' if len(text) > 100 else ''}"
"""

        return resultado_formateado

    except Exception as e:
        return f"❌ Error al analizar con modelo ElSlay: {str(e)}"


@tool
def phishing_analysis_comparison(text: str) -> str:
    """Realiza un análisis comparativo de phishing usando ambos modelos BERT.

    Args:
        text: Texto a analizar (email, URL, SMS o cualquier texto)

    Returns:
        Análisis comparativo con recomendaciones basadas en ambos modelos
    """
    print("Usando herramienta phishing_analysis_comparison")
    try:
        # Validar entrada
        if not text or not text.strip():
            return "❌ Error: El texto no puede estar vacío"

        # Análisis con modelo ealvaradob
        try:
            input_tokens = tokenizer_phishing(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
            output1 = model_ealvaradob(**input_tokens)
            logits1 = output1.logits
            prob1 = logits1.softmax(dim=1)
            pred1_id = argmax(prob1, dim=1)[0].item()
            etiqueta1 = model_ealvaradob.config.id2label[pred1_id]
            confianza1 = prob1[0, pred1_id].item() * 100
            es_phishing1 = etiqueta1 == "phishing"
        except Exception as e:
            return f"❌ Error en modelo ealvaradob: {str(e)}"

        # Análisis con modelo ElSlay
        try:
            resultado2 = model_elslay(text)
            pred2_info = resultado2[0]
            es_phishing2 = pred2_info["label"] == "LABEL_1"
            confianza2 = pred2_info["score"] * 100
        except Exception as e:
            return f"❌ Error en modelo ElSlay: {str(e)}"

        # Análisis comparativo
        ambos_detectan = es_phishing1 and es_phishing2
        ninguno_detecta = not es_phishing1 and not es_phishing2
        #discrepancia = es_phishing1 != es_phishing2

        # Determinar recomendación final
        if ambos_detectan:
            if confianza1 >= 70 and confianza2 >= 70:
                recomendacion = "🚨 ALTO RIESGO - Ambos modelos detectan phishing con alta confianza"
                nivel_final = "CRÍTICO"
            else:
                recomendacion = "⚠️ RIESGO MODERADO - Ambos modelos detectan phishing"
                nivel_final = "ALTO"
        elif ninguno_detecta:
            if confianza1 >= 70 and confianza2 >= 70:
                recomendacion = "✅ BAJO RIESGO - Ambos modelos clasifican como benigno"
                nivel_final = "BAJO"
            else:
                recomendacion = "🤔 REVISAR - Baja confianza en ambos modelos"
                nivel_final = "INCIERTO"
        else:
            recomendacion = "⚠️ DISCREPANCIA - Los modelos no coinciden, revisar manualmente"
            nivel_final = "MODERADO"

        resultado_final = f"""🔍 Análisis Comparativo de Phishing

📊 MODELO EALVARADOB:
   • Resultado: {'🚨 PHISHING' if es_phishing1 else '✅ BENIGNO'}
   • Confianza: {confianza1:.1f}%

📊 MODELO ELSLAY:
   • Resultado: {'🚨 PHISHING' if es_phishing2 else '✅ BENIGNO'}
   • Confianza: {confianza2:.1f}%

🎯 ANÁLISIS FINAL:
   • Nivel de Riesgo: {nivel_final}
   • Recomendación: {recomendacion}

📝 Texto analizado: "{text[:100]}{'...' if len(text) > 100 else ''}"
"""

        return resultado_final

    except Exception as e:
        return f"❌ Error en análisis comparativo: {str(e)}"
