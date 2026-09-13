import json
import re
from typing import Any


FIELDS = ("bug_type", "detected_issue", "explanation", "suggested_fix", "corrected_code", "reason")


def compute_severity(bug_type: str, detected_issue: str = "") -> dict[str, str]:
    bt = str(bug_type or "").lower()
    issue = str(detected_issue or "").lower()
    if any(k in bt or k in issue for k in ("syntax", "parse", "indentation", "fatal", "crash", "semicolon")):
        return {"level": "CRITICAL", "class": "severity-critical"}
    if any(k in bt or k in issue for k in ("runtime", "zerodivision", "indexerror", "nullpointer", "recursion", "divide by zero")):
        return {"level": "HIGH", "class": "severity-high"}
    if any(k in bt or k in issue for k in ("logic", "semantic", "infinite", "off-by-one", "comparison", "smaller")):
        return {"level": "MEDIUM", "class": "severity-medium"}
    if any(k in bt or k in issue for k in ("no obvious issue", "clean", "pass", "no error", "valid")):
        return {"level": "CLEAN", "class": "severity-clean"}
    if any(k in bt or k in issue for k in ("optimization", "performance", "style", "quality", "warning")):
        return {"level": "LOW", "class": "severity-low"}
    return {"level": "INFO", "class": "severity-info"}


def clean_code(text: str) -> str:
    s = str(text or "").strip()
    m = re.match(r"^```[a-zA-Z0-9_-]*\s*\n?(.*?)\n?```$", s, re.DOTALL)
    if m:
        return m.group(1).strip()
    return s


def _to_str(val: Any) -> str:
    if isinstance(val, list):
        return "\n".join(str(x).strip() for x in val if str(x).strip())
    return str(val or "").strip()


def _normalise(data: dict[str, Any]) -> dict[str, str]:
    inner = data.get("response") if isinstance(data.get("response"), dict) else (data.get("result") if isinstance(data.get("result"), dict) else data)
    res = {field: _to_str(inner.get(field, "")) for field in FIELDS}
    res["corrected_code"] = clean_code(res.get("corrected_code", ""))
    sev = compute_severity(res.get("bug_type", ""), res.get("detected_issue", ""))
    res["severity"] = str(inner.get("severity") or data.get("severity") or sev["level"]).strip()
    res["severity_class"] = str(inner.get("severity_class") or data.get("severity_class") or sev["class"]).strip()
    return res


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
    sev = compute_severity(result.get("bug_type", ""), result.get("detected_issue", ""))
    result["severity"] = sev["level"]
    result["severity_class"] = sev["class"]
    return result
