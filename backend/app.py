import logging
from pathlib import Path
import re

from flask import Flask, jsonify, render_template, request

from backend.config import Config
from backend.model_service import ModelError, analyze_with_provider, create_provider


def print_console_report(language: str, code: str, error_message: str, result: dict, latency: float, mode: str):
    divider = "=" * 65
    subdivider = "-" * 65
    print("\n" + divider)
    print("               CODEMATE ANALYSIS REPORT")
    print(divider)
    print(f" Mode     : {mode.upper()}")
    print(f" Language : {language}")
    print(f" Latency  : {latency}s")
    print(f" Severity : {result.get('severity', 'N/A')}")
    print(f" Bug Type : {result.get('bug_type', 'N/A')}")
    if error_message:
        print(f" Error Msg: {error_message}")
    print(subdivider)
    print(" [DETECTED ISSUE(S)]:")
    print(f" {result.get('detected_issue', 'N/A')}")
    print(subdivider)
    print(" [EXPLANATION]:")
    print(f" {result.get('explanation', 'N/A')}")
    print(subdivider)
    print(" [SUGGESTED FIX]:")
    print(f" {result.get('suggested_fix', 'N/A')}")
    print(subdivider)
    print(" [ORIGINAL CODE]:")
    for line in code.strip().splitlines():
        print(f"   | {line}")
    print(subdivider)
    print(" [CORRECTED CODE]:")
    for line in str(result.get('corrected_code', '')).strip().splitlines():
        print(f"   | {line}")
    print(subdivider)
    print(f" [REASON]: {result.get('reason', 'N/A')}")
    print(divider + "\n", flush=True)


def create_app(config_class=Config):
    base_dir = Path(__file__).resolve().parent.parent
    template_dir = base_dir / "frontend" / "templates"
    static_dir = base_dir / "frontend" / "static"

    app = Flask(
        __name__,
        template_folder=str(template_dir),
        static_folder=str(static_dir)
    )
    app.config.from_object(config_class)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    provider = create_provider(app.config)

    @app.get("/")
    def index():
        return render_template("index.html", mode=app.config["MODEL_PROVIDER"])

    @app.get("/about")
    def about():
        return render_template("about.html", mode=app.config["MODEL_PROVIDER"])

    @app.get("/api/health")
    def health():
        return jsonify({
            "status": "ok",
            "model_provider": app.config["MODEL_PROVIDER"],
            "model_name": app.config.get("MODEL_NAME", "unknown")
        })

    @app.post("/api/analyze")
    def api_analyze():
        payload = request.get_json(silent=True) or request.form
        code = str(payload.get("code", ""))
        language = str(payload.get("language", "Python"))[:40]
        error_message = str(payload.get("error_message", ""))[:2000]

        if not code.strip():
            return jsonify({"error": "Please enter code before analyzing."}), 400
        if len(code) > app.config["MAX_CODE_LENGTH"]:
            return jsonify({"error": f"Code is too large. Limit is {app.config['MAX_CODE_LENGTH']} characters."}), 413
        if not re.match(r"^[A-Za-z0-9+#/ -]+$", language):
            return jsonify({"error": "Unsupported language value."}), 400

        try:
            result, latency = analyze_with_provider(provider, language, code, error_message)
        except ModelError as exc:
            return jsonify({"error": str(exc), "mode": app.config["MODEL_PROVIDER"]}), 503
        except Exception as exc:
            return jsonify({"error": f"Analysis unexpected error: {exc}", "mode": app.config["MODEL_PROVIDER"]}), 500

        print_console_report(language, code, error_message, result, latency, app.config["MODEL_PROVIDER"])

        return jsonify({
            "result": result,
            "latency": latency,
            "mode": app.config["MODEL_PROVIDER"]
        })

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
