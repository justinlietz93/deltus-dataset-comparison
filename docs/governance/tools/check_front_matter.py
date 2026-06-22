from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2] / "pages"
missing = []
for path in ROOT.rglob("*.md"):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        missing.append(path)

if missing:
    for path in missing:
        print(f"missing front matter: {path}")
    sys.exit(1)

print("front matter check passed")
