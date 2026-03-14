from typing import List

import google.generativeai as genai

from config import settings

genai.configure(api_key=settings.gemini_api_key)

_model = genai.GenerativeModel("gemini-2.5-flash")

SYSTEM_PROMPT = """You are an intelligent document assistant. 
Answer the user's question strictly based on the provided document context.
Be concise, accurate, and cite specific details from the context.
If the answer is not present in the context, say: "I couldn't find relevant information in the document for this question."
Do NOT make up information outside the provided context."""


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
