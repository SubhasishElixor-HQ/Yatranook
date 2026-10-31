"""Generate a grounded response with Google's official Gen AI Python SDK."""
from google import genai

from rag.config import settings
from rag.generation.prompt_template import build_prompt


def generate_response(question: str, matches: list[dict]) -> str:
    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to your .env file. "
            "Retrieval can still be tested without Gemini; see the README."
        )
    if not matches:
        return (
            "I could not find enough relevant information in the Yatranook tourism "
            "knowledge base to answer that reliably. Please try another question "
            "or add a trusted source document."
        )

    client = genai.Client(api_key=settings.gemini_api_key)
    try:
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=build_prompt(question, matches),
        )
        answer = (response.text or "").strip()
        if not answer:
            raise RuntimeError("The AI model returned an empty response.")
        return answer
    finally:
        client.close()
