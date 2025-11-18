# ia/ai_interpreter.py
import os
import google.generativeai as genai

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("Falta GEMINI_API_KEY en .env")

genai.configure(api_key=API_KEY)


def _format_data(data: dict) -> str:
    parts = [f"{k.capitalize()}: {round(v * 100, 1)}%" for k,
             v in data.items() if isinstance(v, (int, float))]
    return ", ".join(parts) if parts else "Sin datos disponibles."


def generate_source_summary(source_name: str, data: dict) -> str:
    try:
        formatted = _format_data(data)

        prompt = (
            f"Genera una interpretación breve, en tercera persona, "
            f"basada en los indicadores de {source_name}: {formatted}. "
            f"Debe ser una explicación directa de lo que reflejan los datos "
            f"sobre bienestar o desarrollo humano.\n\n"
            f"Reglas estrictas:\n"
            f"- No uses frases como 'como analista', 'según mi análisis', 'en mi rol', 'como modelo', 'esta es tu respuesta'.\n"
            f"- No uses primera persona ('yo', 'mi', 'me').\n"
            f"- No incluyas introducciones, aclaraciones, contexto ni explicaciones del proceso.\n"
            f"- Empieza directamente con la interpretación.\n"
            f"- No uses listas, encabezados ni formato Markdown.\n"
            f"- Solo genera 2–3 líneas de texto corrido.\n"
        )

        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        text = response.text.strip() if response.text else None

        if not text or len(text) < 10:
            raise ValueError()

        return text

    except Exception:
        return "No se pudo generar interpretación para esta fuente."


def generate_detailed_insight(country: str, normalized: dict, sources: dict) -> dict:
    try:
        grouped = {}
        for metric, src in sources.items():
            grouped.setdefault(src, {})[metric] = normalized.get(metric, 0)

        per_source = {src: generate_source_summary(
            src, vals) for src, vals in grouped.items()}

        summary_prompt = (
            f"Basándote en estos análisis parciales para {country}:\n"
            f"{per_source}\n\n"
            f"Escribe un resumen general en el formato:\n"
            f'**Resumen:** ...\n**Interpretación:** ...\n**Reflexión:** ...'
        )

        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(summary_prompt)
        summary_text = response.text.strip(
        ) if response.text else "No se pudo generar resumen general."

        return {"sources": per_source, "summary": summary_text}

    except Exception as e:
        return {"sources": {}, "summary": f"Error al generar insight global: {e}"}
