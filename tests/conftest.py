"""Test helpers for the standalone ScorpionTrack integration repo."""

from __future__ import annotations

import sys
from pathlib import Path


LIBRARY_SRC = Path(__file__).resolve().parents[2] / "python-scorpiontrack" / "src"

if LIBRARY_SRC.exists():
    sys.path.insert(0, str(LIBRARY_SRC))
