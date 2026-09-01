# Contributing to CodeMate

## Development Setup

1. Create a virtual environment:
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

2. Install development dependencies:
   ```powershell
   pip install -e ".[dev]"
   ```

3. Create `.env` file from `.env.example`

## Running Tests

```powershell
# All tests
python -m pytest

# With coverage
python -m pytest --cov=src/codemate

# Specific test file
python -m pytest tests/test_app.py -v
```

## Code Style

- Format code with Black
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions and classes

## Git Workflow

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and commit: `git commit -m "feat: description"`
3. Push and create pull request

## Issue Tracking

Use GitHub Issues for bug reports and feature requests.
