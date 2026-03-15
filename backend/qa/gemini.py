from typing import List

import google.generativeai as genai

from config import settings

genai.configure(api_key=settings.gemini_api_key)

_model = genai.GenerativeModel("gemini-2.5-flash")

SYSTEM_PROMPT = """You are MedQuery AI, an expert clinical AI assistant for doctors and healthcare providers.
Your job is to extract medical insights, histories, and vitals from the provided unstructured patient records.

STRICT RULES:
1. Answer the user's question strictly based on the provided clinical document context.
2. Be concise, highly accurate, and directly address the clinical question. Doctors are pressed for time, so do not include unnecessary filler.
3. ABSOLUTELY NO HALLUCINATION: Never invent or guess medical details, diagnoses, dates, or vitals.
4. If the requested information (e.g. a specific lab value or date) is NOT present in the provided context, state clearly: "Information not found in the current patient record."
5. Present lists, anomalies, or vitals in bullet points for easy scannability where appropriate."""


def generate_answer(question: str, context_chunks: List[str]) -> str:
    """Generate an answer to the question using the provided context chunks."""
    if not context_chunks:
        return "I couldn't find relevant information in the document for this question."

    context = "\n\n---\n\n".join(context_chunks)
    prompt = f"""{SYSTEM_PROMPT}

--- DOCUMENT CONTEXT ---
{context}
--- END CONTEXT ---

User Question: {question}

Answer:"""

    response = _model.generate_content(prompt)
    return response.text.strip()
