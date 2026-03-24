"""
app.py — Streamlit entrypoint for LLaMA 3 Local AI
Run: streamlit run app.py   OR   bash run.sh
"""

import sys
import os

# ── Add project root to sys.path so `src` package is found ────────────────
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# ── Add src/ to sys.path so backend/model imports work inside src/ ─────────
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from src.ui import main

if __name__ == "__main__":
    main()
