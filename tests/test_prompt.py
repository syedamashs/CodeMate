from services.prompt_service import build_prompt


def test_prompt_contains_few_shot_and_input():
    prompt = build_prompt("Python", "print('hello')", "")
    assert "Structured few-shot example" in prompt
    assert "print('hello')" in prompt
    assert "corrected_code" in prompt
