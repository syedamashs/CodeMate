import pytest
from backend.app import create_app
from backend.config import Config
from backend.prompt_service import build_audit_prompt
from backend.response_parser import parse_audit_response


class TestConfig(Config):
    TESTING = True
    MODEL_PROVIDER = "demo"


@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.test_client() as client:
        yield client


def test_build_audit_prompt():
    prompt = build_audit_prompt("Python", "def foo(): pass")
    assert "Algorithmic Complexity" in prompt
    assert "health_score" in prompt
    assert "time_complexity" in prompt
    assert "security_status" in prompt
    assert "def foo(): pass" in prompt


def test_parse_audit_response_json():
    sample = """{
        "health_score": 95,
        "time_complexity": "O(N)",
        "space_complexity": "O(1)",
        "complexity_explanation": "Single linear pass.",
        "security_status": "Safe",
        "security_findings": [],
        "code_smells": ["Missing docstring"],
        "optimization_tips": ["Use generator"],
        "optimized_code": "def foo(): return 1"
    }"""
    parsed = parse_audit_response(sample)
    assert parsed["health_score"] == 95
    assert parsed["health_label"] == "Excellent"
    assert parsed["time_complexity"] == "O(N)"
    assert parsed["space_complexity"] == "O(1)"
    assert parsed["security_status"] == "Safe"
    assert "Missing docstring" in parsed["code_smells"]


def test_parse_audit_response_fenced():
    sample = """```json
    {
        "health_score": 45,
        "time_complexity": "O(N^2)",
        "space_complexity": "O(N)",
        "complexity_explanation": "Nested loops.",
        "security_status": "Vulnerable",
        "security_findings": ["Unsafe eval used"],
        "code_smells": ["Deep nesting"],
        "optimization_tips": ["Refactor to map"],
        "optimized_code": "def foo(): pass"
    }
    ```"""
    parsed = parse_audit_response(sample)
    assert parsed["health_score"] == 45
    assert parsed["health_label"] == "Needs Refactoring"
    assert parsed["time_complexity"] == "O(N^2)"
    assert parsed["security_status"] == "Vulnerable"
    assert "Unsafe eval used" in parsed["security_findings"]


def test_audit_route_get(client):
    res = client.get("/audit")
    assert res.status_code == 200
    assert b"Algorithmic health" in res.data


def test_api_audit_rejects_empty(client):
    res = client.post("/api/audit", json={"code": "", "language": "Python"})
    assert res.status_code == 400
    assert "error" in res.get_json()


def test_api_audit_demo_success(client):
    nested_code = """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
"""
    res = client.post("/api/audit", json={"code": nested_code, "language": "Python"})
    assert res.status_code == 200
    data = res.get_json()
    assert "result" in data
    assert "latency" in data
    assert data["mode"] == "demo"
    result = data["result"]
    assert result["time_complexity"] == "O(N^2)"
    assert "health_score" in result
    assert "security_status" in result
    assert "optimization_tips" in result
