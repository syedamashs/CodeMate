import ast
import json
import logging
import re
import time
import urllib.error
import urllib.request

from codemate.services.prompt_service import build_prompt
from codemate.services.response_parser import parse_response

logger = logging.getLogger(__name__)


class ModelError(RuntimeError):
    """Raised when a configured model cannot produce a response."""


class ModelProvider:
    def analyze(self, language: str, code: str, error_message: str = "") -> dict[str, str]:
        raise NotImplementedError


class APIModelProvider(ModelProvider):
    def __init__(self, api_key: str, model_name: str, base_url: str, timeout: int = 60):
        self.api_key, self.model_name = api_key, model_name
        self.base_url, self.timeout = base_url.rstrip("/"), timeout

    def analyze(self, language: str, code: str, error_message: str = "") -> dict[str, str]:
        if not self.api_key:
            raise ModelError("API provider is selected, but API_KEY is not configured.")
        payload = {"model": self.model_name, "temperature": 0.1, "messages": [
            {"role": "system", "content": "You are CodeMate. Return only the JSON requested by the user."},
            {"role": "user", "content": build_prompt(language, code, error_message)},
        ]}
        request = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = json.loads(response.read().decode("utf-8"))
            return parse_response(body["choices"][0]["message"]["content"])
        except (urllib.error.URLError, KeyError, IndexError, json.JSONDecodeError) as exc:
            raise ModelError(f"The model provider could not complete the request: {exc}") from exc


class LocalModelProvider(ModelProvider):
    def __init__(self, model_name: str):
        self.model_name = model_name
        self._pipeline = None

    def analyze(self, language: str, code: str, error_message: str = "") -> dict[str, str]:
        try:
            from transformers import pipeline
        except ImportError as exc:
            raise ModelError("Transformers is not installed for local model mode.") from exc
        if self._pipeline is None:
            self._pipeline = pipeline("text-generation", model=self.model_name)
        prompt = build_prompt(language, code, error_message)
        generated = self._pipeline(prompt, max_new_tokens=500, do_sample=False)[0]["generated_text"]
        return parse_response(generated[len(prompt):])


class DemoModelProvider(ModelProvider):
    """Clearly labelled offline mode for demonstrations when no model is configured."""

    def analyze(self, language: str, code: str, error_message: str = "") -> dict[str, str]:
        corrected_code = code
        result = {"bug_type": "No obvious issue", "detected_issue": "No obvious issue was found by the offline checks.",
                  "explanation": "Demo Mode performs a small, deterministic syntax and runtime-risk scan. Configure an API or local model for Transformer analysis.",
                  "suggested_fix": "Review the code with the configured model provider for deeper analysis.",
                  "corrected_code": corrected_code, "reason": "The offline scanner did not identify a supported defect."}
        if language.lower() == "python":
            try:
                ast.parse(code)
            except SyntaxError as exc:
                corrected_code = re.sub(r"^(\s*def\s+[^\n:]+)(\s*)$", r"\1:\2", code, flags=re.MULTILINE)
                result.update(bug_type="Syntax Error", detected_issue=f"{exc.msg} on line {exc.lineno}.",
                              explanation="Python could not parse the source because its syntax is incomplete or invalid.",
                              suggested_fix="Add the missing syntax, such as the colon after a function definition.", reason="The Python AST parser rejected the input.", corrected_code=corrected_code)
            else:
                if "/0" in code.replace(" ", "") or "divide(10, 0)" in code:
                    corrected_code = code.replace("return a / b", "if b == 0:\n        raise ValueError('b must not be zero')\n    return a / b")
                    corrected_code = corrected_code.replace("divide(10, 0)", "divide(10, 1)")
                    result.update(bug_type="Runtime Error", detected_issue="The code attempts to divide by zero.",
                                  explanation="Division by zero raises ZeroDivisionError at runtime.", suggested_fix="Validate the denominator before dividing.",
                                  reason="The denominator is the literal value zero.", corrected_code=corrected_code)
                elif "max_value = 0" in code and "if n < max_value" in code:
                    corrected_code = code.replace("max_value = 0", "max_value = numbers[0] if numbers else 0").replace("if n < max_value", "if n > max_value")
                    result.update(bug_type="Logical Error", detected_issue="The comparison updates max_value when a number is smaller.",
                                  explanation="This returns zero for all-positive inputs and does not compute the maximum.", suggested_fix="Use `if n > max_value` and initialize from the input when negatives are valid.",
                                  reason="Maximum tracking requires replacing the current value with larger numbers.", corrected_code=corrected_code)
        elif language.lower() in {"c", "c++"} and re.search(r"return\s+a\s*\+\s*b\s*}", code):
            corrected_code = re.sub(r"(return\s+a\s*\+\s*b)\s*}", r"\1; }", code)
            result.update(bug_type="Syntax Error", detected_issue="The return statement is missing a semicolon.",
                          explanation="C requires a semicolon to terminate a return statement.", suggested_fix="Add the missing semicolon before the closing brace.",
                          reason="The C statement is not terminated.", corrected_code=corrected_code)
        elif language.lower() == "java" and re.search(r"System\.out\.println\([^;]+\)", code):
            corrected_code = re.sub(r"(System\.out\.println\([^;]+\))(?!;)", r"\1;", code)
            if corrected_code != code:
                result.update(bug_type="Syntax Error", detected_issue="The println statement is missing a semicolon.",
                              explanation="Java statements must end with semicolons.", suggested_fix="Add the missing semicolon.",
                              reason="The Java statement is not terminated.", corrected_code=corrected_code)
        if error_message:
            result["detected_issue"] += f" Supplied error: {error_message[:300]}"
        return result


def create_provider(config) -> ModelProvider:
    get = config.get if hasattr(config, "get") else lambda key: getattr(config, key)
    provider = get("MODEL_PROVIDER")
    if provider == "api":
        return APIModelProvider(get("API_KEY"), get("MODEL_NAME"), get("API_BASE_URL"), get("MODEL_TIMEOUT"))
    if provider == "local":
        return LocalModelProvider(get("MODEL_NAME"))
    return DemoModelProvider()


def analyze_with_provider(provider: ModelProvider, language: str, code: str, error_message: str = "") -> tuple[dict[str, str], float]:
    started = time.perf_counter()
    logger.info("Model request started provider=%s", provider.__class__.__name__)
    result = provider.analyze(language, code, error_message)
    latency = round(time.perf_counter() - started, 3)
    logger.info("Model response received latency=%ss", latency)
    return result, latency
