# ----------------------------------------
# Purpose:
# Executes final infrastructure decision and logs pipeline data
#
# Why:
# This is the final stage where system takes action and stores audit logs
#
# Flow:
# Load drift -> Load AI -> Get decision -> Execute -> Log to MongoDB
# ----------------------------------------

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from backend.db.mongo_client import get_logs_collection
from backend.decision.decision_engine import get_user_decision


def execute_pipeline():
    """Main function to run Stage 5 execution and Mongo logging."""
    project_root = Path(__file__).resolve().parents[2]
    logs_dir = project_root / "logs"
    terraform_dir = project_root / "terraform"

    drift_file = logs_dir / "drift.json"
    ai_file = logs_dir / "ai_response.json"

    if not drift_file.exists():
        raise FileNotFoundError(f"Missing file: {drift_file}")
    if not ai_file.exists():
        raise FileNotFoundError(f"Missing file: {ai_file}")

    drift_data = json.loads(drift_file.read_text(encoding="utf-8"))
    ai_data = json.loads(ai_file.read_text(encoding="utf-8"))
    decision = get_user_decision()

    try:
        if decision.get("action") == "revert":
            subprocess.run(
                ["terraform", "apply", "-auto-approve"],
                cwd=terraform_dir,
                check=True,
                capture_output=True,
                text=True,
            )
            print("Terraform apply completed")
        else:
            print("Keeping current infrastructure")
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.strip() if exc.stderr else str(exc)
        raise RuntimeError(f"Terraform execution failed: {message}") from exc

    payload = {
        "drift": drift_data,
        "ai_response": ai_data,
        "decision": decision,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    try:
        get_logs_collection().insert_one(payload)
    except Exception as exc:
        raise RuntimeError(f"MongoDB logging failed: {exc}") from exc

    print("✅ Logged to MongoDB Atlas")
    return payload
