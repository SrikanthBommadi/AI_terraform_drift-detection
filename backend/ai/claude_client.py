"""
Purpose:
- Provide an AI analysis layer for Terraform drift results.

Why AI is used:
- Terraform plan JSON is large and technical. AI helps convert it into
  an actionable decision: KEEP or REVERT, with short reasoning and suggested
  Terraform changes when keeping the drift.

Flow:
1) Read `logs/drift.json` produced by Stage 2.
2) Build a simple, structured prompt for drift review.
3) Call Claude API through REST using `requests` and `CLAUDE_API_KEY`.
4) Save Claude response to `logs/ai_response.json`.
5) Return response JSON to caller.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv


def analyze_drift_with_ai() -> dict:
    """Analyze Terraform drift JSON with Claude and store AI output."""
    project_root = Path(__file__).resolve().parents[2]
    load_dotenv(project_root / ".env")

    logs_dir = project_root / "logs"
    drift_file = logs_dir / "drift.json"
    ai_output_file = logs_dir / "ai_response.json"

    if not drift_file.exists():
        raise FileNotFoundError(f"Drift file not found: {drift_file}")

    api_key = os.getenv("CLAUDE_API_KEY")
    if not api_key:
        raise ValueError("CLAUDE_API_KEY is not set.")

    drift_data = json.loads(drift_file.read_text(encoding="utf-8"))

    prompt = (
        "You are a Terraform drift analysis assistant.\n"
        "Analyze the following Terraform plan JSON and respond in JSON format.\n\n"
        "Required response schema:\n"
        "{\n"
        '  "decision": "KEEP or REVERT",\n'
        '  "reasoning": "short explanation",\n'
        '  "terraform_changes_if_keep": ["change 1", "change 2"]\n'
        "}\n\n"
        "Drift JSON:\n"
        f"{json.dumps(drift_data)}"
    )

    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "anthropic-beta": "messages-2023-12-15",
            "content-type": "application/json",
        },
        json={
            "model": "claude-sonnet-4-6",
            "max_tokens": 1200,
            "temperature": 0,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=120,
    )
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        error_payload = {
            "status_code": response.status_code,
            "response_text": response.text,
        }
        logs_dir.mkdir(parents=True, exist_ok=True)
        ai_output_file.write_text(json.dumps(error_payload, indent=2), encoding="utf-8")
        raise RuntimeError(f"Claude API request failed: {response.status_code}") from exc

    data = response.json()
    logs_dir.mkdir(parents=True, exist_ok=True)
    ai_output_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return data
