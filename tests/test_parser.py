from backend.response_parser import parse_response


def test_parser_json():
    result = parse_response('{"bug_type":"Syntax Error","detected_issue":"Missing colon"}')
    assert result["bug_type"] == "Syntax Error"
    assert result["severity"] == "CRITICAL"
    assert result["severity_class"] == "severity-critical"


def test_parser_fallback():
    result = parse_response("BUG_TYPE: Runtime Error\nEXPLANATION: It crashes")
    assert result["bug_type"] == "Runtime Error"
    assert result["explanation"] == "It crashes"
    assert result["severity"] == "HIGH"
