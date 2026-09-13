from backend.prompt_service import build_prompt


def test_prompt_contains_instructions_and_input():
    prompt = build_prompt("Python", "print('hello')", "")
    assert "CRITICAL INSTRUCTIONS" in prompt
    assert "print('hello')" in prompt
    assert "corrected_code" in prompt
