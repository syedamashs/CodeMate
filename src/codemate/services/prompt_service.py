import json


SYSTEM_PROMPT = """You are CodeMate, an expert software-engineering coding assistant.
Analyze source code carefully for syntax, logical, runtime, and code-quality issues.
Explain issues clearly for a student. Suggest a correction and provide corrected code.
Do not claim code is correct without sufficient evidence. Do not reveal hidden reasoning.
Return only valid JSON with the requested keys."""

FEW_SHOT_EXAMPLE = {
    "language": "Python",
    "code": "def greet(name)\n    return 'Hello ' + name",
    "error_message": "",
    "response": {
        "bug_type": "Syntax Error",
        "detected_issue": "The function definition is missing a colon.",
        "explanation": "Python requires a colon at the end of a def statement before its indented body.",
        "suggested_fix": "Add a colon after the closing parenthesis.",
        "corrected_code": "def greet(name):\n    return 'Hello ' + name",
        "reason": "The colon makes the function header syntactically complete.",
    },
}


def build_prompt(language: str, code: str, error_message: str = "") -> str:
    example = json.dumps(FEW_SHOT_EXAMPLE, ensure_ascii=True)
    return f"""{SYSTEM_PROMPT}

Structured few-shot example:
{example}

Programming language: {language}
User error message: {error_message or "None provided"}
Source code:
```{language.lower()}
{code}
```

Return a JSON object with exactly these string keys:
bug_type, detected_issue, explanation, suggested_fix, corrected_code, reason.
Use concise, verifiable explanations. Preserve the user's language and intent.
"""
