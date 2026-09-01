# CodeMate - Code Analysis and Evaluation Tool

CodeMate is a Flask web application for Assignment 1, 22ITRM0 (Large Language Models). It accepts code and an optional error message, builds a structured few-shot prompt, calls a replaceable model provider, parses the response, and presents a bug explanation and corrected code.

## 📁 Project Structure

```
Code-Mate/
├── src/
│   └── codemate/              # Main Python package
│       ├── __init__.py
│       ├── app.py             # Flask application factory
│       ├── config.py          # Configuration management
│       ├── services/          # Business logic and providers
│       │   ├── __init__.py
│       │   ├── dataset_service.py
│       │   ├── model_service.py
│       │   ├── prompt_service.py
│       │   └── response_parser.py
│       ├── evaluation/        # Evaluation harness
│       │   ├── __init__.py
│       │   └── evaluator.py
│       └── utils/             # Utility functions
├── tests/                     # Test suite
├── datasets/                  # Data files
├── static/                    # Frontend assets
├── templates/                 # HTML templates
├── docs/                      # Documentation
├── .github/workflows/         # CI/CD workflows
├── requirements.txt
├── pyproject.toml
├── pytest.ini
├── .env.example
└── README.md
```

## 🚀 Quick Start

### Installation

```powershell
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

```powershell
# Create .env from example
Copy-Item .env.example .env

# Edit .env for your configuration:
# - DEMO mode (default): works without API key
# - API mode: set MODEL_PROVIDER=api, MODEL_NAME, API_KEY
# - Local mode: set MODEL_PROVIDER=local and MODEL_NAME
```

### Running the Application

```powershell
cd src
python -m codemate.app
```

Open http://127.0.0.1:5000 in your browser.

## 🧪 Testing

```powershell
python -m pytest -q
python -m pytest --cov=src/codemate
```

## 📊 Datasets

- **CodeSearchNet**: Arrow shards under `datasets/codesearchnet/`
- **HumanEval**: `datasets/humaneval/human-eval-master/data/HumanEval.jsonl.gz`
- **MBPP**: Loaded via `datasets.load_dataset("mbpp")`, capped by `MBPP_SAMPLE_SIZE`

Dataset loading is informational and controlled. The application never executes user or model-generated code.

## 🔧 Configuration

Set environment variables in `.env` (see `.env.example` for all options):

| Variable | Default | Purpose |
|----------|---------|---------|
| `MODEL_PROVIDER` | `demo` | Model provider: `demo`, `api`, or `local` |
| `MODEL_NAME` | `gpt-4o-mini` | Model identifier |
| `API_KEY` | `` | API key for remote models |
| `MAX_CODE_LENGTH` | `12000` | Max input code length (chars) |
| `MODEL_TIMEOUT` | `60` | Response timeout (seconds) |

## 📖 Documentation

- [API Reference](docs/API.md)
- [Contributing Guide](docs/CONTRIBUTING.md)

## 👥 Team

Mohanalingam M, Praveen M, Syed Amash S
