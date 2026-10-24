"""Low-dependency structural checks for local development."""
from pathlib import Path
import compileall

ROOT = Path(__file__).resolve().parents[1]
required = ["app.py", "config.py", "app/templates/base.html", "app/static/css/styles.css", "app/static/files/milad-ahmad-hakimi-cv.pdf"]
missing = [path for path in required if not (ROOT / path).is_file()]
if missing:
    raise SystemExit("Missing required files: " + ", ".join(missing))
if not compileall.compile_dir(ROOT / "app", quiet=1):
    raise SystemExit("Python compilation failed")
print("Project structure and Python compilation checks passed.")
