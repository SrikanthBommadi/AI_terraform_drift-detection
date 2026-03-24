"""
Purpose:
- Centralize environment-based configuration used by backend modules.

Why this file exists:
- Keeping env access in one place avoids duplicated key names and makes
  MongoDB setup consistent across files.

Flow:
1) Load `.env` from project root.
2) Read Mongo configuration values.
3) Expose a helper for typed config access.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


def get_mongo_config() -> dict:
    """Return MongoDB connection settings from environment."""
    return {
        "uri": os.getenv("MONGO_URI", "").strip(),
        "db_name": os.getenv("MONGO_DB_NAME", "drift_detect").strip(),
        "collection_name": os.getenv("MONGO_COLLECTION_NAME", "pipeline_logs").strip(),
    }
