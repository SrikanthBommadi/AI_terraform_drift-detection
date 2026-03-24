"""
Purpose:
- Persist decision pipeline logs into MongoDB Atlas.

Why this file exists:
- Stage outputs should be stored durably for audit and troubleshooting.

Flow:
1) Build a minimal log document.
2) Insert document into Mongo collection.
3) Return inserted document id.
"""

from __future__ import annotations

from datetime import datetime, timezone

from backend.db.mongo_client import get_logs_collection


def save_pipeline_log(
    ai_decision: str,
    user_action: str,
    status: str,
    error: str | None = None,
) -> str:
    """Save one pipeline log entry and return inserted id."""
    doc = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "ai_decision": ai_decision,
        "user_action": user_action,
        "status": status,
        "error": error,
    }
    result = get_logs_collection().insert_one(doc)
    return str(result.inserted_id)
