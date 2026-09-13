import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from backend.app import app, create_app

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)

