from backend.app import create_app
from backend.config import Config


class TestConfig(Config):
    MODEL_PROVIDER = "demo"


def test_home_route():
    client = create_app(TestConfig).test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"CodeMate" in response.data


def test_analyze_rejects_empty_code():
    client = create_app(TestConfig).test_client()
    response = client.post("/api/analyze", json={"code": ""})
    assert response.status_code == 400
    assert "Please enter code" in response.get_json()["error"]


def test_demo_analysis():
    client = create_app(TestConfig).test_client()
    response = client.post("/api/analyze", json={"language": "Python", "code": "def add(a, b)\n    return a + b"})
    assert response.status_code == 200
    result = response.get_json()["result"]
    assert result["bug_type"] == "Syntax Error"
    assert result["corrected_code"] == "def add(a, b):\n    return a + b"


def test_c_and_java_demo_corrections():
    client = create_app(TestConfig).test_client()
    c_result = client.post("/api/analyze", json={"language": "C", "code": "int add(int a, int b) { return a + b }"}).get_json()["result"]
    java_result = client.post("/api/analyze", json={"language": "Java", "code": 'class Main { System.out.println("Hello") }'}).get_json()["result"]
    assert "; }" in c_result["corrected_code"]
    assert 'println("Hello");' in java_result["corrected_code"]
