import json
import re
from typing import Any


FIELDS = ("bug_type", "detected_issue", "explanation", "suggested_fix", "corrected_code", "reason")


def _normalise(data: dict[str, Any]) -> dict[str, str]:
    return {field: str(data.get(field, "")).strip() for field in FIELDS}


def parse_response(raw_response: str) -> dict[str, str]:
    text = raw_response.strip()
    candidates = [text]
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL | re.IGNORECASE)
    if fenced:
        candidates.insert(0, fenced.group(1))
    json_match = re.search(r"\{.*\}", text, re.DOTALL)
    if json_match:
        candidates.insert(0, json_match.group(0))
    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            result = _normalise(parsed)
            if any(result.values()):
                return result

    result = {field: "" for field in FIELDS}
    labels = {
        "bug_type": r"BUG_TYPE\s*:\s*(.*?)(?=\n[A-Z_]+\s*:|$)",
        "detected_issue": r"DETECTED_ISSUE\s*:\s*(.*?)(?=\n[A-Z_]+\s*:|$)",
        "explanation": r"EXPLANATION\s*:\s*(.*?)(?=\n[A-Z_]+\s*:|$)",
        "suggested_fix": r"(?:FIX|SUGGESTED_FIX)\s*:\s*(.*?)(?=\n[A-Z_]+\s*:|$)",
        "corrected_code": r"CORRECTED_CODE\s*:\s*(.*?)(?=\n[A-Z_]+\s*:|$)",
        "reason": r"REASON\s*:\s*(.*?)(?=\n[A-Z_]+\s*:|$)",
    }
    for field, pattern in labels.items():
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            result[field] = match.group(1).strip().strip("`")
    if not any(result.values()):
        result["explanation"] = text or "The model returned an empty response."
        result["bug_type"] = "Unclassified"
    return result
