"""
Purpose of decision layer:
- Convert AI analysis into a clear, operator-confirmed runtime decision.

Why human approval is needed:
- AI guidance can be helpful, but infrastructure changes should still require
  explicit human confirmation to reduce accidental risk.

Flow:
1) Read `logs/ai_response.json` from Stage 3.
2) Extract AI decision and reasoning from the response text.
3) Show both values in CLI.
4) Ask user to choose KEEP or REVERT.
5) If KEEP, ask approval for Terraform changes (yes/no).
6) Return final decision payload.
"""

from __future__ import annotations

import json
from pathlib import Path

from backend.db.logger import save_pipeline_log


def _extract_ai_json_text(ai_response: dict) -> dict:
    """Extract JSON block from Claude text response."""
    content = ai_response.get("content", [])
    if not content:
        return {}

    text = content[0].get("text", "")
    if "```json" in text:
        text = text.split("```json", 1)[1].split("```", 1)[0]
    return json.loads(text.strip())


def get_user_decision() -> dict:
    """Show AI suggestion, collect user decision, and return final action."""
    project_root = Path(__file__).resolve().parents[2]
    ai_file = project_root / "logs" / "ai_response.json"

    if not ai_file.exists():
        raise FileNotFoundError(f"AI response file not found: {ai_file}")

    ai_response = json.loads(ai_file.read_text(encoding="utf-8"))
    ai_data = _extract_ai_json_text(ai_response)

    ai_decision = ai_data.get("decision", "UNKNOWN")
    ai_reason = ai_data.get("reasoning", "No reasoning found.")

    print(f"AI decision: {ai_decision}")
    print(f"Reason: {ai_reason}")

    while True:
        choice = input("Choose action (KEEP/REVERT): ").strip().lower()
        if choice in {"keep", "revert"}:
            break
        print("Invalid input. Enter KEEP or REVERT.")

    approved = False
    if choice == "keep":
        while True:
            approval = input("Do you approve Terraform changes? (yes/no): ").strip().lower()
            if approval in {"yes", "no"}:
                approved = approval == "yes"
                break
            print("Invalid input. Enter yes or no.")

    status = "approved" if approved else "not_approved"
    if choice == "revert":
        status = "revert_selected"

    error_message = None
    try:
        save_pipeline_log(
            ai_decision=ai_decision,
            user_action=choice,
            status=status,
            error=error_message,
        )
    except Exception as exc:  # Keep CLI flow independent from DB availability.
        error_message = str(exc)
        print(f"Mongo log save failed: {error_message}")

    return {"action": choice, "approved": approved}
