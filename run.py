#!/usr/bin/env python
"""
CodeMate Entry Point

Run the Flask application. Can be invoked as:
  python run.py
  python -m codemate.app
  flask run
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from codemate.app import app

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
