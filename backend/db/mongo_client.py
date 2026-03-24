"""
Purpose:
- Create MongoDB Atlas collection handle for logging pipeline events.

Why this file exists:
- Connection setup should be isolated from business logic so decision/AI
  modules only call a simple helper.

Flow:
1) Read Mongo config from `backend/config.py`.
2) Open MongoClient using Atlas URI.
3) Return target collection object.
"""

from __future__ import annotations

from pymongo import MongoClient

from backend.config import get_mongo_config


def get_logs_collection():
    """Return MongoDB collection used to store pipeline logs."""
    cfg = get_mongo_config()
    if not cfg["uri"]:
        raise ValueError("MONGO_URI is not set.")

    client = MongoClient(cfg["uri"], serverSelectionTimeoutMS=10000)
    return client[cfg["db_name"]][cfg["collection_name"]]
