# ----------------------------------------
# Purpose:
# Single entrypoint to run the complete drift-detection pipeline
#
# Why:
# Provides one command to execute detect -> analyze -> decide -> execute -> log
#
# Flow:
# Stage 2 plan -> Stage 3 AI -> Stage 5 execute (includes Stage 4 decision)
# ----------------------------------------

from __future__ import annotations

from backend.ai.claude_client import analyze_drift_with_ai
from backend.executor.terraform_executor import execute_pipeline
from backend.plan.planner import run_terraform_plan


def run_pipeline():
    """Run all implemented stages in order."""
    print("Running Stage 2: Terraform drift detection...")
    run_terraform_plan()

    print("Running Stage 3: AI drift analysis...")
    analyze_drift_with_ai()

    print("Running Stage 4/5: Decision, execution, and Mongo logging...")
    result = execute_pipeline()

    print("Pipeline completed successfully.")
    return result


if __name__ == "__main__":
    run_pipeline()
