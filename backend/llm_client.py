import requests
import json

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5:1.5b"


def call_qwen(prompt: str) -> str:
    """Send a prompt to the local Qwen model via Ollama and return raw text response."""
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False,
        "options": {
            "temperature": 0.2  # low temp = more consistent, less creative drift
        }
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=120)
    response.raise_for_status()
    data = response.json()
    return data["message"]["content"]


def extract_json(raw_text: str) -> dict:
    """
    Qwen sometimes wraps JSON in markdown fences or adds extra text.
    This strips that and parses defensively.
    """
    text = raw_text.strip()

    # Remove markdown code fences if present
    if "```" in text:
        parts = text.split("```")
        for part in parts:
            part = part.strip()
            if part.startswith("json"):
                part = part[4:].strip()
            if part.startswith("{"):
                text = part
                break

    # Find the first { and last } to isolate JSON object
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1:
        text = text[start:end + 1]

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Fallback: handle smart quotes / stray trailing commas
    cleaned = text.replace("\u201c", '"').replace("\u201d", '"')
    cleaned = cleaned.replace(",\n}", "\n}").replace(",\n  }", "\n  }")
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        return {
            "error": f"Failed to parse model output as JSON: {str(e)}",
            "raw_output": raw_text
        }
