# Migration Guide: New Project Structure

## What Changed?

The project has been reorganized from a flat structure to a professional Python package layout:

### Old Structure
```
Code-Mate/
├── app.py
├── config.py
├── services/
├── evaluation/
└── ...
```

### New Structure
```
Code-Mate/
├── src/
│   └── codemate/
│       ├── app.py
│       ├── config.py
│       ├── services/
│       ├── evaluation/
│       └── utils/
├── tests/
├── docs/
└── ...
```

## Running the Application

### Before
```powershell
python app.py
```

### After
```powershell
# Option 1: Direct run
python run.py

# Option 2: Module run
python -m codemate.app

# Option 3: Flask run (after setting FLASK_APP)
$env:FLASK_APP = "src/codemate/app.py"
flask run
```

## Import Changes

All imports in service and evaluation files have been updated to use the new package structure:

```python
# Old
from config import Config
from evaluation.evaluator import run_evaluation

# New
from codemate.config import Config
from codemate.evaluation.evaluator import run_evaluation
```

## Testing

Tests have been moved and should now be run from the project root:

```powershell
python -m pytest tests/
```

## Configuration

- Copy `.env.example` to `.env`
- Configuration paths are now relative to the project root via `ROOT_DIR`
- All existing environment variables work unchanged

## File Locations

| What | Where |
|------|-------|
| Main application | `src/codemate/app.py` |
| Configuration | `src/codemate/config.py` |
| Services | `src/codemate/services/` |
| Evaluation | `src/codemate/evaluation/` |
| Tests | `tests/` |
| Datasets | `datasets/` (unchanged) |
| Static files | `static/` (unchanged) |
| Templates | `templates/` (unchanged) |
| Documentation | `docs/` (NEW) |

## Benefits of New Structure

1. **Professional Layout**: Follows Python packaging standards
2. **Installable Package**: Can be installed with `pip install -e .`
3. **Better Testing**: Tests can be run from anywhere
4. **Clear Separation**: Source code isolated in `src/` directory
5. **Scalability**: Easier to add new modules and services
6. **Documentation**: Dedicated `docs/` folder
7. **CI/CD Ready**: Structure supports automated workflows
8. **Type Checking**: Compatible with mypy and other type checkers

## Troubleshooting

### "ModuleNotFoundError: No module named 'codemate'"

Make sure you're running from the project root and have `src/` in PYTHONPATH:

```powershell
$env:PYTHONPATH = "src"
python run.py
```

Or use the module run syntax:
```powershell
python -m codemate.app
```

### "Template not found"

The Flask app now uses relative paths to find templates:
- Ensure you're running from the project root
- Templates are at `templates/` (same as before)

### "Dataset files not found"

- Datasets remain at `datasets/` (unchanged)
- Paths in config.py are automatically resolved relative to project root

## Next Steps

1. Update any external scripts that import from this project
2. Run tests to ensure everything works: `python -m pytest tests/`
3. Update CI/CD pipelines to use new entry point: `python run.py`
4. Consider adding GitHub Actions workflows (skeleton provided in `.github/workflows/`)
