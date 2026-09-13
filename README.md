# CodeMate - AI Code Intelligence & Automated Review Workbench

CodeMate is a modern web application for intelligent source code analysis and automated debugging. Powered by local Ollama language models (e.g. `qwen2.5-coder:1.5b`), it inspects code for syntax errors, runtime risks, and logical flaws, explains root causes, produces line-by-line visual diffs, and provides one-click export reports.

## 📁 Project Structure

```
Code-Mate/
├── backend/                   # Flask backend service
│   ├── app.py                 # Application factory & API endpoints
│   ├── config.py              # Environment configuration loader
│   ├── model_service.py       # Ollama, OpenAI-compatible & Demo providers
│   ├── prompt_service.py      # Structured prompting engine
│   └── response_parser.py     # Resilient JSON parser & severity analyzer
├── frontend/                  # Modern UI & workbench
│   ├── static/
│   │   ├── css/style.css      # Custom dark/warm design tokens & layout
│   │   └── js/app.js          # Diff computation, Prism highlighting, console logging
│   └── templates/
│       ├── base.html          # Base layout & sidebar navigation
│       ├── index.html         # Code analysis lab & visual diff workbench
│       └── about.html         # Architecture overview & team information
├── tests/                     # Fast automated pytest suite
│   ├── pytest.ini             # Pytest configuration
│   ├── test_app.py            # API integration tests
│   ├── test_parser.py         # Parser & JSON recovery tests
│   └── test_prompt.py         # Prompt engineering tests
├── TESTCASES.md               # Ready-to-use testing catalog (12 test cases)
├── app.py                     # Root entry point
├── requirements.txt           # Python dependencies
└── .env                       # Environment configuration
```

## 🚀 Quick Start

### 1. Prerequisites & Ollama Model
Install [Ollama](https://ollama.com/) and pull a code-specialized model:
```powershell
ollama pull qwen2.5-coder:1.5b
```

### 2. Installation
```powershell
# Create & activate virtual environment (optional)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Set up your `.env` file:
```ini
MODEL_PROVIDER=ollama
MODEL_NAME=qwen2.5-coder:1.5b
OLLAMA_BASE_URL=http://127.0.0.1:11434
MODEL_TIMEOUT=120
```

### 4. Running the Application
```powershell
python app.py
```
Open **http://127.0.0.1:5000** in your browser.

---

## 🧪 Testing

Run the automated test suite:
```powershell
python -m pytest tests/
```
All tests run in isolated demo mode and pass in ~0.15s.

---

## ✨ Features
- **Local AI Inference:** Zero external cloud data leakage using local Ollama.
- **Side-by-Side Visual Diff:** Dynamic LCS-based diff viewer highlighting line additions and deletions.
- **Syntax Highlighting & Line Numbers:** Multi-language highlighting via Prism.js.
- **Defect Severity Tagging:** Automatic classification (Critical, High, Medium, Low/Clean).
- **Dual Console Reporting:** Terminal stdout reports and Browser DevTools (F12) formatted logs.
- **One-Click Export:** Download corrected source code or complete Markdown review reports.

---

## 👥 Engineering Team
- Mohanalingam M
- Praveen M
- Syed Amash S

