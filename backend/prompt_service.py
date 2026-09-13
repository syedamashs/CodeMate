SYSTEM_PROMPT = """You are CodeMate, an expert code reviewer and software engineer.
Your task is to analyze the user's source code with strict precision.

CRITICAL INSTRUCTIONS:
1. NEVER hallucinate bugs that do not exist.
   - If the code has a colon (:), DO NOT say it is missing!
   - If strings and parentheses are properly closed, DO NOT say they are missing!
2. Analysis Priority:
   - First check SYNTAX: are there genuine syntax errors (unclosed brackets, unclosed strings, missing colons, missing semicolons)?
   - Next check RUNTIME RISKS: division by zero, empty collection operations, null pointers, out-of-bounds indices, infinite recursion.
   - Next check LOGIC: wrong operators (< instead of >), inverted conditions, off-by-one errors.
   - If the code is already correct and bug-free, set bug_type to "No obvious issue", detected_issue to "No bugs detected", and return the code as-is.
3. Be specific: explain the REAL root cause of the bug and provide the working fixed code.
4. Return ONLY valid JSON with no preamble."""


def build_prompt(language: str, code: str, error_message: str = "") -> str:
    err_context = f"Error traceback / message:\n{error_message.strip()}\n" if error_message.strip() else ""
    return f"""{SYSTEM_PROMPT}

Programming Language: {language}
{err_context}
Source code to analyze:
```{language.lower()}
{code}
```

Return a JSON object with exactly these string keys:
- bug_type: category of issue (e.g. "Syntax Error", "Runtime Error", "Logical Error", or "No obvious issue")
- detected_issue: specific defect(s) found in this exact code
- explanation: clear explanation of why this bug occurs
- suggested_fix: how to resolve the issue
- corrected_code: the complete, working fixed code
- reason: why this fix works
"""

