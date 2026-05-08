import json
import os
from dotenv import load_dotenv

load_dotenv()


def openai_enabled() -> bool:
    return os.getenv("USE_OPENAI", "false").lower() == "true" and bool(os.getenv("OPENAI_API_KEY"))


def llm_provider() -> str:
    if openai_enabled():
        return f"OpenAI {os.getenv('OPENAI_MODEL', 'gpt-4o-mini')}"
    return "Demo mode, deterministic response"


def ask_openai(task: str, question: str, metrics: dict, allowed_values: list[str]) -> str:
    """
    Optional LLM call.

    Safe design:
    The prompt tells OpenAI to only use allowed numeric values.
    The citation guard still checks the final output afterwards.
    """
    if not openai_enabled():
        return ""

    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    system = (
        "You are a concise enterprise trading assistant. "
        "Use only the allowed numeric values. "
        "Do not invent numbers. "
        "If asked to forecast future revenue, refuse because no approved forecast model is available."
    )

    payload = {
        "task": task,
        "question": question,
        "metrics": metrics,
        "allowed_numeric_values": allowed_values,
        "format": "plain text, concise, Teams-ready",
    }

    response = client.chat.completions.create(
        model=model,
        temperature=0.1,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(payload)},
        ],
    )

    return response.choices[0].message.content or ""
