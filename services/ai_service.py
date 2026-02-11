import json
from typing import Any, Dict

try:
    import google.generativeai as genai
except ImportError:  # pragma: no cover - handled at runtime
    genai = None


def _build_prompt(signal: Dict[str, Any], asset: Dict[str, Any], market: Dict[str, Any]) -> str:
    return (
        "You are a crypto trading analyst. Analyze the intraday signal and market snapshot. "
        "Return a raw JSON object only (no code fences, no markdown) with keys: "
        "summary, recommendation, confidence, risks. "
        "confidence must be a number between 0 and 1. risks must be a list of strings.\n\n"
        f"Signal: {json.dumps(signal)}\n"
        f"Asset: {json.dumps(asset)}\n"
        f"Market: {json.dumps(market)}\n"
    )


def _strip_code_fences(text: str) -> str:
    if "```" not in text:
        return text
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```", 2)[1]
    if cleaned.endswith("```"):
        cleaned = cleaned.rsplit("```", 1)[0]
    return cleaned.strip()


def generate_insight(
    api_key: str,
    model_name: str,
    signal: Dict[str, Any],
    asset: Dict[str, Any],
    market: Dict[str, Any],
) -> Dict[str, Any]:
    if not api_key:
        return {
            "summary": "Missing GEMINI_API_KEY.",
            "recommendation": "Set GEMINI_API_KEY in .env.",
            "confidence": 0.0,
            "risks": ["AI provider not configured"],
        }

    if genai is None:
        return {
            "summary": "google-generativeai is not installed.",
            "recommendation": "Install dependencies from requirements.txt.",
            "confidence": 0.0,
            "risks": ["AI provider library missing"],
        }

    genai.configure(api_key=api_key) # Before you can use the AI, you have to prove you have permission. This line sends your unique API Key to Google's servers. It’s like swiping a badge at the entrance of a lab so you can use their equipment.
    model = genai.GenerativeModel(model_name=model_name)  # This line creates an instance of the AI model you want to use. It’s like choosing which machine you want to work with in the lab. The model_name should match one of the available Gemini models, such as "gemini-1.5-flash".
    prompt = _build_prompt(signal, asset, market)
    response = model.generate_content(prompt)
    text = getattr(response, "text", "") or ""  # This line tries to get the "text" attribute from the response object. If for some reason the response doesn't have a "text" attribute or it's None, it defaults to an empty string. This is a safety measure to prevent errors when processing the response.
    text = _strip_code_fences(text)  # Some AI models return their output wrapped in markdown code fences (```), especially when they are asked to return JSON. This function removes those fences so that you can parse the text as JSON without issues.

    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        payload = {
            "summary": text.strip() or "No response.",
            "recommendation": "Review summary.",
            "confidence": 0.0,
            "risks": ["Model did not return JSON"],
        }

    # The AI might return incomplete data, so we set defaults to ensure the payload always has the expected structure.
    # If the key is already there, setdefault does absolutely nothing. It leaves the AI's original data alone.
    payload.setdefault("summary", "")
    payload.setdefault("recommendation", "")
    payload.setdefault("confidence", 0.0)
    payload.setdefault("risks", [])

    return payload
