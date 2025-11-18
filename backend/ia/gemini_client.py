import os
import google.generativeai as genai

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("Falta GEMINI_API_KEY en .env")

genai.configure(api_key=API_KEY, client_options={"api_key": API_KEY})


def generate_insight(data: dict) -> str:
    prompt = f"""
Eres un analista de bienestar del proyecto QualiLife AI. 
Genera el análisis del país solicitado EXCLUSIVAMENTE en el formato indicado al final.
No incluyas introducciones, frases contextuales, explicaciones del proceso, resúmenes previos,
confirmaciones, frases como "Aquí tienes tu respuesta", "Resultado:", "Output:", 
"Segun lo solicitado", "A continuación", ni ningún texto ajeno al formato estrictamente requerido.

Datos:
- País: {data['country']}
- QLI: {data['qli']:.3f}
- Economía: {data.get('economy', 0):.3f}
- Salud: {data.get('health', 0):.3f}
- Clima: {data.get('climate', 0):.3f}
- Seguridad: {data.get('safety', 0):.3f}
- Educación: {data.get('education', 0):.3f}
- Conectividad: {data.get('connectivity', 0):.3f}
- Igualdad: {data.get('equality', 0):.3f}

Reglas:
- No agregues texto antes ni después del formato.
- No incluyas notas, conclusiones adicionales o explicaciones.
- No uses emojis.
- No uses frases meta de modelo ("Esta es tu respuesta", "Generado por IA", etc.).
- No agregues advertencias ni introducciones.
- No reformules los encabezados.
- No escribas nada fuera del formato esperado.
- Mantén tono humano, claro, no técnico, sin política.

FORMATO ESTRICTO (responde solo esto):
**Resumen:** [1–2 líneas]
**Interpretación:** [explicación basada en los factores]
**Reflexión:** [mensaje constructivo y práctico]
"""

    model = genai.GenerativeModel("gemini-2.5-pro")
    response = model.generate_content(prompt)
    if not response.text:
        return "No se pudo generar una interpretación con formato estructurado."

    text = response.text.strip().replace("\n\n", "\n").strip()

    # Validación estricta del formato
    if not (
        text.startswith("**Resumen:**")
        and "**Interpretación:**" in text
        and "**Reflexión:**" in text
    ):
        fail_msg = "No se pudo generar una interpretación válida con formato estructurado."
        try:
            response2 = model.generate_content(prompt)
            text2 = response2.text.strip().replace("\n\n", "\n").strip()
            if (
                text2.startswith("**Resumen:**")
                and "**Interpretación:**" in text2
                and "**Reflexión:**" in text2
            ):
                return text2
        except:
            pass
        return fail_msg

    return text
