import logging
import re

from flask import Flask, jsonify, render_template, request

from codemate.config import Config
from codemate.evaluation.evaluator import run_evaluation
from codemate.services.dataset_service import DatasetService
from codemate.services.model_service import ModelError, analyze_with_provider, create_provider


def create_app(config_class=Config):
    app = Flask(__name__, template_folder="../../templates", static_folder="../../static")
    app.config.from_object(config_class)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    provider = create_provider(app.config)
    dataset_service = DatasetService(app.config)

    @app.get("/")
    def index():
        return render_template("index.html", mode=app.config["MODEL_PROVIDER"])

    @app.get("/evaluate")
    def evaluate():
        return render_template("evaluate.html", mode=app.config["MODEL_PROVIDER"])

    @app.get("/datasets")
    def datasets():
        return render_template("datasets.html", datasets=dataset_service.summaries(), mode=app.config["MODEL_PROVIDER"])

    @app.get("/about")
    def about():
        return render_template("about.html", mode=app.config["MODEL_PROVIDER"])

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok", "model_provider": app.config["MODEL_PROVIDER"]})

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
        return jsonify({"result": result, "latency": latency, "mode": app.config["MODEL_PROVIDER"]})

    @app.post("/api/evaluate")
    def api_evaluate():
        payload = request.get_json(silent=True) or {}
        try:
            samples = int(payload.get("samples", 10))
        except (TypeError, ValueError):
            return jsonify({"error": "Samples must be a number."}), 400
        if samples < 1 or samples > 100:
            return jsonify({"error": "Samples must be between 1 and 100."}), 400
        return jsonify(run_evaluation(provider, str(payload.get("dataset", "MBPP")), samples, dataset_service))

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
