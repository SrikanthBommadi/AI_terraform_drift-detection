"""
Purpose:
- Run Terraform plan-based drift detection and export machine-readable output.

Why this file exists:
- This stage uses Terraform's native `plan` output to detect drift between
  real infrastructure and declared state.
- We use `terraform plan` + `terraform show -json` instead of driftctl because
  Terraform is already part of this project workflow, requires no extra tool,
  and produces JSON that can be consumed directly by later stages.

Flow of execution:
1) Resolve project paths (`terraform/` input, `logs/` output).
2) Ensure `logs/` folder exists.
3) Run `terraform plan -out=tfplan` inside `terraform/`.
4) Run `terraform show -json tfplan`.
5) Parse JSON and save it to `logs/drift.json`.
6) Return parsed JSON data to caller.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


def run_terraform_plan() -> dict:
    """Run Terraform plan, save JSON drift output, and return parsed data."""
    project_root = Path(__file__).resolve().parents[2]
    terraform_dir = project_root / "terraform"
    logs_dir = project_root / "logs"
    drift_file = logs_dir / "drift.json"

    logs_dir.mkdir(parents=True, exist_ok=True)

    try:
        subprocess.run(
            ["terraform", "plan", "-out=tfplan"],
            cwd=terraform_dir,
            check=True,
            capture_output=True,
            text=True,
        )
        show_result = subprocess.run(
            ["terraform", "show", "-json", "tfplan"],
            cwd=terraform_dir,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.strip() if exc.stderr else str(exc)
        raise RuntimeError(f"Terraform command failed: {message}") from exc

    data = json.loads(show_result.stdout)
    drift_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return data
